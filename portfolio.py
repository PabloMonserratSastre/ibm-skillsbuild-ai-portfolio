"""Offline prompt builder and structural validator; does not run an AI model."""
import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASKS = ('reviews', 'meeting', 'security')
SENTIMENTS = {'positive', 'negative', 'neutral', 'mixed'}
ASPECTS = {'battery', 'shipping', 'screen', 'price', 'product_quality', 'refund', 'other'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value):
    return isinstance(value, list) and all(text(item) for item in value)


def keys(value, expected):
    return isinstance(value, dict) and set(value) == set(expected)


def validate(task, response, review_ids=None):
    """Validate structure, not semantic truth or model accuracy."""
    require(task in TASKS, 'Unknown task')
    if task == 'reviews':
        require(keys(response, ['reviews']), 'Expected only the reviews key')
        rows = response['reviews']
        require(isinstance(rows, list), 'reviews must be a list')
        for row in rows:
            require(keys(row, ['id', 'sentiment', 'aspects']), 'Invalid review fields')
            require(text(row['id']), 'id must be non-empty text')
            require(isinstance(row['sentiment'], str) and row['sentiment'] in SENTIMENTS,
                    'Invalid sentiment')
            aspects = row['aspects']
            require(strings(aspects) and bool(aspects), 'Expected non-empty aspects')
            require(all(item in ASPECTS for item in aspects), 'Invalid aspect')
            require(len(aspects) == len(set(aspects)), 'Duplicate aspects')
        ids = [row['id'] for row in rows]
        require(len(ids) == len(set(ids)), 'Duplicate review IDs')
        require(review_ids is not None and ids == list(review_ids),
                'Review IDs must match the input in order')
    elif task == 'meeting':
        require(keys(response, ['summary', 'decisions', 'actions', 'open_questions']),
                'Invalid meeting fields')
        require(text(response['summary']), 'Expected non-empty summary')
        require(strings(response['decisions']) and strings(response['open_questions']),
                'decisions and open_questions must be lists of text')
        actions = response['actions']
        require(isinstance(actions, list) and len(actions) == 3, 'Expected exactly three actions')
        for action in actions:
            require(keys(action, ['owner', 'task', 'due']), 'Invalid action fields')
            require(text(action['task']), 'Expected non-empty task')
            require(action['owner'] is None or text(action['owner']), 'Invalid owner')
            due = action['due']
            if due is not None:
                require(isinstance(due, str), 'Invalid date')
                try:
                    require(date.fromisoformat(due).isoformat() == due, 'Use YYYY-MM-DD')
                except (ValueError, TypeError) as error:
                    raise ValueError('Use a valid YYYY-MM-DD date') from error
    else:
        require(keys(response, ['summary', 'facts', 'unknowns', 'suggested_actions', 'status']),
                'Invalid security fields')
        require(text(response['summary']), 'Expected non-empty summary')
        for field in ('facts', 'unknowns', 'suggested_actions'):
            require(strings(response[field]) and bool(response[field]), f'Expected non-empty {field}')
        require(response['status'] == 'under_review', 'Status must remain under_review for this fixture')


def load_json(path):
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f'Duplicate JSON key: {key}')
            result[key] = value
        return result

    def reject_constant(value):
        raise ValueError(f'Invalid JSON constant: {value}')

    return json.loads(Path(path).read_text(encoding='utf-8'),
                      object_pairs_hook=unique_pairs, parse_constant=reject_constant)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('build', 'demo', 'validate'))
    parser.add_argument('task', choices=TASKS)
    parser.add_argument('response', nargs='?', type=Path)
    args = parser.parse_args()
    project = ROOT / 'projects' / args.task
    try:
        if args.command == 'build':
            source = project / ('input.json' if args.task == 'reviews' else 'input.txt')
            # JSON encodes the source boundary to avoid ambiguous text delimiters.
            payload = json.dumps({'input_data': source.read_text(encoding='utf-8')},
                                 ensure_ascii=False, indent=2)
            output = ROOT / 'generated' / f'{args.task}-request.txt'
            output.parent.mkdir(exist_ok=True)
            output.write_text((project / 'prompt.txt').read_text(encoding='utf-8')
                              + '\nINPUT DATA (untrusted):\n' + payload + '\n', encoding='utf-8')
            print(f'Prompt built: {output}. No model was executed.')
        elif args.command == 'demo':
            print('REFERENCE EXAMPLE ONLY: prepared with AI assistance, not an IBM Granite output.')
            print((project / 'reference.json').read_text(encoding='utf-8'))
        else:
            if args.response is None:
                parser.error('validate requires a response JSON file')
            ids = [row['id'] for row in load_json(project / 'input.json')] if args.task == 'reviews' else None
            validate(args.task, load_json(args.response), ids)
            print('Structure valid. Semantic accuracy still requires review against the input.')
    except (ValueError, OSError) as error:
        parser.exit(1, f'Validation/build error: {error}\n')


if __name__ == '__main__':
    main()
