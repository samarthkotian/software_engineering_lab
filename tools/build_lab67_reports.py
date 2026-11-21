"""Build submission PDFs using captured live-terminal screenshots."""
from pathlib import Path
from PIL import Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak, Preformatted
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

REPO = Path(__file__).resolve().parents[1]
styles = getSampleStyleSheet()
styles['BodyText'].fontSize = 10
styles['BodyText'].leading = 15
styles['Title'].textColor = colors.HexColor('#16324f')
styles['Heading1'].textColor = colors.HexColor('#16324f')
styles['Code'].fontSize = 7.5
styles['Code'].leading = 10
styles['Code'].leftIndent = 0
def evidence(folder, name):
    path=folder/'evidence'/f'{name}.png'
    if not path.is_file():
        raise FileNotFoundError(f'Capture the live terminal screenshot first: {path}')
    return path

def footer(canvas,doc):
    canvas.setFont('Helvetica',8)
    canvas.setFillColor(colors.HexColor('#5e6c78'))
    canvas.drawString(42,25,'Samarth Kotian | PES1UG24CS406 | Software Engineering')
    canvas.drawRightString(A4[0]-42,25,str(doc.page))

def para(text): return Paragraph(text,styles['BodyText'])
def title(text): return Paragraph(text,styles['Title'])
def h(text): return Paragraph(text,styles['Heading1'])
def shot(story,path):
    w,hh=Image.open(path).size
    width=510
    height=hh*width/w
    if height>600:
        width*=600/height
        height=600
    story.extend([RLImage(str(path),width,height),Spacer(1,10)])

def make6():
    folder=REPO/'lab6'
    line=evidence(folder,'line_coverage')
    branch=evidence(folder,'branch_coverage')
    story=[title('Lab 6: Code and Branch Coverage'),para('Salon Booking | Samarth Kotian | PES1UG24CS406 | Section 5G'),
        Spacer(1,15),h('Objective and source'),
        para('Measure baseline coverage, then add independent tests to achieve at least 90% line and branch coverage. The assigned Lab 6 application is unchanged.'),
        para('Assigned source: https://github.com/SETAPESU26/L6_L7_42_salon_booking'),
        h('Measured results'),
        para('Initial tests: 2 passed; 14/37 statements executed (37.84%, displayed as 38%). In branch mode, coverage.py displayed a combined statement-and-branch score of 32%; that column is not the branch-only percentage.'),
        para('Final line suite: 14 passed; 37/37 statements covered (100%). Final branch suite: 71 passed; 37/37 statements and 26/26 branch exits covered (100%), with zero missing or partial branches.'),
        h('Test design'),
        para('The line suite reaches every executable statement, including both validation exceptions, rate selection, member allowance, long-session surcharge, booking rejection, and every arrival result. The branch suite checks all services, both membership states, junior/senior stylists, and extra minutes 0, 1, 60 and 61. Booking tests cross party limits 2 and 4 and the service limit 2. Arrival tests use the exact cutoff, one minute below, cutoff minus 15, and cutoff minus 16 on weekdays and weekends.'),
        h('Interpretation'),
        para('Line coverage asks whether a statement ran. Branch coverage asks whether decision exits ran; executing every statement can still leave false outcomes untested. Path coverage concerns combinations of decisions and can be much larger. Function coverage records whether each function was called. All three application functions were exercised here. High coverage does not prove correctness; expected-value assertions are still required.'),
        para('The evidence images are actual screenshots of a live xterm browser terminal displaying the Python test commands and their process output. The commands were run locally against the assigned application before each screenshot. Both final coverage results exceed 90%. Raw capture transcripts, initial and final analysis logs, and machine-readable coverage JSON are retained in reports/.'),
        PageBreak(),h('Final line coverage evidence'),
        para('<b>Final line coverage: 100% - 37 of 37 statements; 14 tests passed.</b>'),Spacer(1,10)]
    shot(story,line)
    story.extend([PageBreak(),h('Final branch coverage evidence'),
                  para('<b>Final branch coverage: 100% - 26 of 26 branch exits; 71 tests passed.</b>'),Spacer(1,10)])
    shot(story,branch)
    story.extend([h('Reproduce'),Preformatted('python -m pip install pytest coverage\npython -m coverage run --source=salon_booking -m pytest CodeCoverageTest_salon_booking.py\npython -m coverage report -m\npython -m coverage run --branch --source=salon_booking -m pytest BranchCoverageTest_salon_booking.py\npython -m coverage report -m',styles['Code'])])
    for label, filename in [
        ('Appendix A: Code coverage Python test file', 'CodeCoverageTest_salon_booking.py'),
        ('Appendix B: Branch coverage Python test file', 'BranchCoverageTest_salon_booking.py'),
    ]:
        story.extend([PageBreak(), h(label), para(filename), Spacer(1,10),
                      Preformatted((folder/filename).read_text(encoding='utf-8'),
                                   styles['Code'], maxLineLength=108)])
    output=folder/'output/pdf'
    output.mkdir(parents=True,exist_ok=True)
    SimpleDocTemplate(str(output/'Lab6_PES1UG24CS406_Coverage.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=40,bottomMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)

def make7():
    folder=REPO/'lab7'
    before=evidence(folder,'before_application')
    fail=evidence(folder,'before_fuzz')
    after=evidence(folder,'after_application')
    final=evidence(folder,'after_fuzz')
    story=[title('Lab 7: Fuzz Testing and Input Validation'),para('Salon Booking | Samarth Kotian | PES1UG24CS406 | Section 5G'),Spacer(1,15),
        h('Objective and method'),para('Complete Hypothesis tests for parse_booking, duration_average and payable_bill, record failures against the original program, repair validation, and run exactly the same test suite against the fixed program. The supplied file is named salon_booking.py; test_processor.py follows the handout naming, and test_salon_booking.py is a compatibility entry point.'),
        para('Assigned source: https://github.com/SETAPESU26/L6_L7_42_salon_booking'),
        h('Measured results'),para('Original: 38 failed, 4 passed. Fixed: 42 passed. Six Hypothesis properties each completed 300 passing examples (1,800 generated examples in the final run), alongside 35 invalid-input regression cases and one documented-example test. Tests use deterministic generation, no example database, and no deadline to make replay stable.'),
        h('Bugs and fixes'),para('All three original functions call split directly, so None and other non-string inputs raise AttributeError. Empty or malformed strings cause unpacking or numeric-conversion ValueError. Hypothesis minimized failures to empty text and None. Explicit regressions also exposed negative values, unknown services, empty CSV elements, NaN, infinity, numeric overflow and oversized integers.'),
        para('The repair validates text and separators before conversion, rejects empty tokens, restricts services to haircut/colour/spa, checks finite nonnegative values, handles conversion failures, and caps input length at 10,000 characters. Every invalid helper input returns None. The interactive program prints an error and continues to the next prompt; EOF or cancellation exits cleanly.'),
        h('Preserved behavior and properties'),para('Valid bookings still return a title-cased service and float duration. CSV averages still use integer floor division. Billing still applies bill * 1.18 - discount, floored at zero. The example haircut:45 returns (Haircut, 45.0), 30,45,60 averages to 45, and 800|100 yields 844.0. Properties check no unexpected exceptions, valid output shape, average bounds and exact integer means, and the billing formula.'),
        para('Design decisions: nonnegative zero durations and prices are allowed; discounts above the taxed bill produce zero. Billing retains binary floating point because that is the assigned API. Fuzzing samples a large input space and does not prove every possible input correct.'),
        para('The evidence images are actual screenshots of a live xterm browser terminal connected to locally executed Python commands. The original application was run in an isolated folder with the same completed tests used for the fixed application. The failing-test screenshot uses concise pytest output; full failure tracebacks, minimized inputs, Hypothesis statistics and capture transcripts are retained in reports/.'),
        PageBreak(),h('1. Original application output')]
    shot(story,before)
    story.extend([PageBreak(),h('2. Fuzz tests before fixes')]);shot(story,fail)
    story.extend([PageBreak(),h('3. Fixed application output')]);shot(story,after)
    story.extend([PageBreak(),h('4. Fuzz tests after fixes')]);shot(story,final)
    story.extend([h('Reproduce'),Preformatted('python -m pip install pytest hypothesis\npython salon_booking.py\npython -m pytest test_processor.py -v --hypothesis-show-statistics',styles['Code']),para('The original application and incomplete starter test are retained in original/. To reproduce baseline failures, run the completed test_processor.py against original/salon_booking.py in an isolated folder. Do not run the incomplete starter test as a valid test suite.')])
    story.extend([
        PageBreak(), h('5. Observations'),
        Paragraph('Original application', styles['Heading2']),
        para('Valid inputs produced the expected booking, average and bill. Malformed input exposed missing validation: a blank booking caused a ValueError, while None caused AttributeError because the functions called split without checking the input type. The same completed suite recorded 38 failed tests and 4 passing tests before the repair.'),
        Paragraph('Inputs uncovered by testing', styles['Heading2']),
        para('Hypothesis reduced failures to small reproducible inputs such as empty text and None. Explicit regression cases additionally checked missing or repeated separators, empty CSV elements, unknown services, negative numbers, NaN, infinity, oversized integer strings and bill overflow. These cases showed that accepting numeric conversion alone was insufficient to validate a booking or bill.'),
        Paragraph('Fixed application', styles['Heading2']),
        para('After adding validation, all 42 tests passed. Each of the six Hypothesis properties completed 300 passing examples, for 1,800 generated passing examples in total. Invalid helper input returned None, and the interactive application printed a validation message and continued to the next prompt.'),
        Paragraph('Valid behavior retained', styles['Heading2']),
        para('haircut:45 still returned (Haircut, 45.0); 30,45,60 still averaged to 45; and 800|100 still produced a payable bill of 844.0. Separate valid-input properties checked the booking result, integer mean and billing formula, so a function that simply returned None for every input would fail the suite.'),
        Paragraph('Inference and limitation', styles['Heading2']),
        para('The observed failures and subsequent passing tests support the validation fixes for the tested input classes. Fuzzing does not exhaust every possible input, and the result depends on the properties and strategies specified.'),
        PageBreak(), h('6. Reflection'),
        Paragraph('What did fuzzing discover?', styles['Heading2']),
        para('The original functions assumed their arguments were well-formed strings. Hypothesis shrank the failures to empty text and None: empty text causes unpacking or conversion errors, while None has no split method. Targeted regression inputs then exposed accepted negative values, unknown services, non-finite floats, malformed CSV fields and overflow. Generated failures and manually chosen regression cases are distinguished in the saved test output.'),
        Paragraph('How did the repair address these bugs?', styles['Heading2']),
        para('Shared validation checks the input type, text length, number of fields and empty tokens before conversion. Numeric conversion failures are handled, and finite/nonnegative checks enforce the input contract. The helpers return None for invalid input; the CLI reports that result and continues. The original booking format, integer floor average and billing formula remain valid.'),
        Paragraph('Why use fuzzing, and what are its limits?', styles['Heading2']),
        para('Examples such as haircut:45 do not test malformed input. Generated Unicode and mixed types explore cases that are easy to overlook, and shrinking makes the smallest failure straightforward to reproduce. No-crash checks alone could also accept an implementation that always returns None, so separate valid-input properties assert the actual booking, average and billing results. Finite sampling and the chosen properties still leave possible untested behaviors.'),
        para('These reflections supplement the listed deliverables; the provided handout does not list separate reflection questions.'),
    ])
    for label, filename in [('Appendix A: Fixed application', 'salon_booking.py'),
                            ('Appendix B: Completed tests', 'test_processor.py')]:
        story.extend([PageBreak(), h(label),
                      Preformatted((folder/filename).read_text(encoding='utf-8'),
                                   styles['Code'], maxLineLength=108)])
    output=folder/'output/pdf';output.mkdir(parents=True,exist_ok=True)
    SimpleDocTemplate(str(output/'Lab7_PES1UG24CS406_Fuzz_Testing.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=40,bottomMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)

if __name__ == '__main__':
    make6();make7()
    print('Built both PDF reports using the six captured terminal screenshots.')
