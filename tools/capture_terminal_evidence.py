"""Run real lab commands in a terminal, pausing for six window screenshots.

The capture controller creates <stage>.continue files in the control directory
after each screenshot. No terminal output is painted or reconstructed here.
"""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import time

REPO = Path(__file__).resolve().parents[1]
CONTROL = REPO.parents[1] / 'terminal_capture_control'
CONTROL.mkdir(exist_ok=True)
BEFORE = CONTROL / 'original_lab7'
BEFORE.mkdir(exist_ok=True)
shutil.copy2(REPO / 'lab7/original/salon_booking.py', BEFORE / 'salon_booking.py')
shutil.copy2(REPO / 'lab7/test_processor.py', BEFORE / 'test_processor.py')


def command(folder, arguments, inputs=None, expected=0):
    print('> python ' + ' '.join(arguments), flush=True)
    if inputs is not None:
        print('Inputs supplied at the prompts: ' + repr(inputs), flush=True)
    result = subprocess.run([sys.executable, *arguments], cwd=folder,
                            input=inputs, text=True, encoding='utf-8',
                            errors='replace', stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    print(result.stdout, end='', flush=True)
    print(f'Exit code: {result.returncode}\n', flush=True)
    if result.returncode != expected:
        raise RuntimeError(f'Unexpected result for {arguments!r}')
    return '> python ' + ' '.join(arguments) + '\n' + result.stdout + f'\nExit code: {result.returncode}\n'


def stage(name, title, jobs):
    selected = os.environ.get('LAB_CAPTURE_ONLY')
    if selected and name != selected:
        return
    (CONTROL / f'{name}.continue').unlink(missing_ok=True)
    # ANSI clear is interpreted by the real Windows Terminal, not an image API.
    print('\033[2J\033[H', end='', flush=True)
    print(f'{title} | Samarth Kotian | PES1UG24CS406\n', flush=True)
    output = ''
    for folder, arguments, inputs, expected in jobs:
        output += command(folder, arguments, inputs, expected)
    lab = 'lab6' if name in ('line_coverage', 'branch_coverage') else 'lab7'
    (REPO / lab / 'reports' / f'screenshot_{name}.txt').write_text(output, encoding='utf-8')
    print('Screenshot ready. Waiting for capture...', flush=True)
    (CONTROL / f'{name}.ready').write_text('ready', encoding='utf-8')
    while not (CONTROL / f'{name}.continue').exists():
        time.sleep(0.2)


def main():
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    l6, l7 = REPO / 'lab6', REPO / 'lab7'
    stage('line_coverage', 'Lab 6 - Final line coverage', [
        (l6, ['-m','coverage','run','--source=salon_booking','-m','pytest',
              'CodeCoverageTest_salon_booking.py','-q'], None, 0),
        (l6, ['-m','coverage','report','-m','--fail-under=90'], None, 0),
    ])
    stage('branch_coverage', 'Lab 6 - Final branch coverage', [
        (l6, ['-m','coverage','run','--branch','--source=salon_booking','-m','pytest',
              'BranchCoverageTest_salon_booking.py','-q'], None, 0),
        (l6, ['-m','coverage','report','-m','--fail-under=90'], None, 0),
    ])
    stage('before_application', 'Lab 7 - Original application', [
        (BEFORE, ['salon_booking.py'], 'haircut:45\n30,45,60\n800|100\n', 0),
        (BEFORE, ['salon_booking.py'], '\n1,,3\nnan|0\n', 1),
    ])
    stage('before_fuzz', 'Lab 7 - Tests before validation fixes', [
        (BEFORE, ['-m','pytest','test_processor.py','-q','--tb=no','--no-summary'], None, 1),
    ])
    stage('after_application', 'Lab 7 - Fixed application', [
        (l7, ['salon_booking.py'], 'haircut:45\n30,45,60\n800|100\n', 0),
        (l7, ['salon_booking.py'], '\n1,,3\nnan|0\n', 0),
    ])
    stage('after_fuzz', 'Lab 7 - Tests after validation fixes', [
        (l7, ['-m','pytest','test_processor.py','-q'], None, 0),
    ])
    print('Requested terminal commands completed.', flush=True)
    (CONTROL / 'complete.ready').write_text('complete', encoding='utf-8')
    time.sleep(2)


if __name__ == '__main__':
    main()
