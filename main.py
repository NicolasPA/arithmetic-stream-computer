from typing import Tuple, Optional

ALLOWED_OPERATORS = ["+", "-", "*", "/"]
PRINT_MESSAGE = "?"


def compute_inside_parentheses(
        user_input: str,
        digit_concatenation: str,
        previous_character: Optional[str],
        operator: Optional[str],
        previous_result: Optional[int],
        result: Optional[int],
        previous_number_evaluation: int,
        previous_term: Optional[int],
        previous_operator: Optional[str],
        term: Optional[int],
        previous_factor: Optional[int],
) -> Tuple[str, str, str, int, int, int, int, str, int, int]:
    """
    Compute the result of a parentheses-free arithmetic expression passed character by character in the user_input
    variable.
    The various precedent results required to compute the next result update are computed and returned, so they can be
    used in the next call.


    :param user_input: a character from a valid arithmetic expression
    :param digit_concatenation: concatenation of digits to make a multi-digit number
    :param previous_character: previous value of user_input
    :param operator: currently active operator
    :param previous_result: previous result computed
    :param result: currently active result
    :param previous_number_evaluation: previous number evaluated in the expression
    :param previous_term: previous addition/subtraction term
    :param previous_operator: previous arithmetic operator
    :param term: currently active addition/subtraction term
    :param previous_factor: previous multiplication/division factor
    :return:
    """
    user_input = user_input.strip()

    if result is None and previous_character is None:
        if not user_input.isdigit() and user_input not in ["(", "-"]:
            raise Exception("First character should be a digit, '(' or '-'.")

    if user_input.isdigit():
        digit_concatenation = digit_concatenation + user_input
        number_evaluation = int(digit_concatenation)

        if result is None or operator is None:
            result = number_evaluation
            previous_result = result

        elif result is not None and operator is not None:
            if operator in ["+", "-"]:
                result = evaluate_operation(previous_result, operator, number_evaluation)
                previous_term = previous_result
                previous_operator = operator
                term = number_evaluation
            else:
                if previous_factor is None:
                    previous_factor = previous_number_evaluation
                elif previous_character in ["*", "/"]:
                    # digit concatenation is done, we can recompute previous factor
                    previous_factor = evaluate_operation(previous_factor, previous_operator, previous_number_evaluation)

                term = evaluate_operation(previous_factor, operator, number_evaluation)
                if previous_term is not None:
                    result = evaluate_operation(
                        previous_term,
                        previous_operator,
                        term
                    )
                else:
                    result = term
                previous_result = result

    elif user_input in ALLOWED_OPERATORS:
        if previous_character in ALLOWED_OPERATORS or previous_character is None:
            if user_input != "-":  # allow negative numbers
                raise Exception(
                    f"It is not allowed to chain two operators {previous_character} and {user_input} except for a "
                    f"negative number."
                )
            else:
                # it's a negative number
                previous_result = result
                digit_concatenation = "-"
        else:
            previous_result = result
            # digit concatenation ends when an operator appears
            previous_number_evaluation = int(digit_concatenation) if digit_concatenation else None
            previous_operator = operator
            operator = user_input
            digit_concatenation = ""

            if operator in ["+", "-"]:
                # new term so reset previous_factor
                previous_factor = None

    elif user_input == PRINT_MESSAGE:
        print(f"Result: {result}")

    elif user_input in ["(", ")"]:
        pass

    else:
        raise Exception(
            f"Input character '{user_input}' is not among the allowed characters: digits, operators between digits "
            f"{ALLOWED_OPERATORS}, parentheses or print result with '{PRINT_MESSAGE}'"
        )

    previous_character = user_input

    return digit_concatenation, previous_character, operator, previous_result, result, previous_number_evaluation, \
        previous_term, previous_operator, term, previous_factor


def evaluate_operation(left: int, operator: str, right: int) -> int:
    """
    Since we decided to not use eval(), this translates an operator character into an actual operation.
    """
    if operator == '+':
        return left + right
    elif operator == '-':
        return left - right
    elif operator == '*':
        return left * right
    elif operator == '/':
        return left // right
    else:
        raise Exception(f"Operator '{operator}' is not supported.")


def handle_parentheses(
        parenthesis_input: str,
        opened_parentheses_counter: Optional[int],
        parentheses_content_concatenation: str,
        digit_concatenation: str,
        previous_character: Optional[str],
        operator: Optional[str],
        previous_result: Optional[int],
        result: Optional[int],
        previous_number_evaluation: int,
        previous_term: Optional[int],
        previous_operator: Optional[str],
        term: Optional[int],
        previous_factor: Optional[int],
) -> Tuple[Optional[int], str, str, str, str, int, int, int, int, str, int, int]:
    """
    Compute the result of an arithmetic expression passed character by character in the user_input
    variable, including with parentheses.

    As it uses compute_inside_parentheses(), the various precedent results required to compute the next result update
    are computed and returned, so they can be used in the next call.
    Except it also has additional accumulators to manage the parentheses.

    :param parenthesis_input: a character from a valid arithmetic expression, including parentheses
    :param opened_parentheses_counter: number of opened parentheses that must be closed before computation can happen.
    :param parentheses_content_concatenation: concatenation of the characters inside the parentheses.
    """
    if parenthesis_input == ")":
        if opened_parentheses_counter is None or opened_parentheses_counter == 0:
            raise Exception(f"Can't close parentheses that weren't opened.")

    if parenthesis_input == PRINT_MESSAGE and opened_parentheses_counter is not None and opened_parentheses_counter != 0:
        raise Exception(f"Can't compute if parentheses remain opened.")

    elif parenthesis_input == "(":
        opened_parentheses_counter = (
            opened_parentheses_counter + 1
            if opened_parentheses_counter is not None
            else 1
        )
    elif parenthesis_input == ")":
        opened_parentheses_counter -= 1

        # todo: compute inner parenthesis

    if opened_parentheses_counter is None:
        outputs = compute_inside_parentheses(
            parenthesis_input,
            digit_concatenation,
            previous_character,
            operator,
            previous_result,
            result,
            previous_number_evaluation,
            previous_term,
            previous_operator,
            term,
            previous_factor,
        )
        return (opened_parentheses_counter, parentheses_content_concatenation) + outputs  # noqa
    elif opened_parentheses_counter == 0:
        opened_parentheses_counter = None
        parentheses_content_concatenation += parenthesis_input

        # evaluate the inside of the parentheses
        _digit_concatenation = ""
        _previous_character = None
        _operator = None
        _previous_result = None
        _result = None
        _previous_number_evaluation = None
        _previous_term = None
        _previous_operator = None
        _term = None
        _previous_factor = None

        for parenthesis_input in parentheses_content_concatenation:
            (
                _digit_concatenation,
                _previous_character,
                _operator,
                _previous_result,
                _result,
                _previous_number_evaluation,
                _previous_term,
                _previous_operator,
                _term,
                _previous_factor
            ) = compute_inside_parentheses(
                parenthesis_input,
                _digit_concatenation,
                _previous_character,
                _operator,
                _previous_result,
                _result,
                _previous_number_evaluation,
                _previous_term,
                _previous_operator,
                _term,
                _previous_factor,
            )

        parentheses_content_concatenation = ""
        parentheses_result = _result
        parenthesis_inputs = str(parentheses_result)
        previous_character = operator

        for parenthesis_input in str(parenthesis_inputs):
            (
                digit_concatenation,
                previous_character,
                operator,
                previous_result,
                result,
                previous_number_evaluation,
                previous_term,
                previous_operator,
                term,
                previous_factor,
            ) = compute_inside_parentheses(
                parenthesis_input,
                digit_concatenation,
                previous_character,
                operator,
                previous_result,
                result,
                previous_number_evaluation,
                previous_term,
                previous_operator,
                term,
                previous_factor,
            )
        return (
            opened_parentheses_counter,
            parentheses_content_concatenation,
            digit_concatenation,
            previous_character,
            operator,
            previous_result,
            result,
            previous_number_evaluation,
            previous_term,
            previous_operator,
            term,
            previous_factor
        )

    else:
        parentheses_content_concatenation += parenthesis_input
        return (
            opened_parentheses_counter,
            parentheses_content_concatenation,
            digit_concatenation,
            previous_character,
            operator,
            previous_result,
            result,
            previous_number_evaluation,
            previous_term,
            previous_operator,
            term,
            previous_factor
        )


def main():
    """
    CLI based user interface to test the app manually.
    """

    opened_parentheses_counter = None
    parentheses_content_concatenation = ""
    digit_concatenation = ""
    previous_character = None
    operator = None
    previous_result = None
    result = None
    previous_number_evaluation = None
    previous_term = None
    previous_operator = None
    term = None
    previous_factor = None

    while True:
        user_input = input(
            f"Please input an integer arithmetic expression with digits [0-9], operators {ALLOWED_OPERATORS} and "
            f"parentheses, character by character. Input '?' to display the current result. \n: "
        )
        (
            opened_parentheses_counter,
            parentheses_content_concatenation,
            digit_concatenation,
            previous_character,
            operator,
            previous_result,
            result,
            previous_number_evaluation,
            previous_term,
            previous_operator,
            term,
            previous_factor
        ) = handle_parentheses(
            user_input,
            opened_parentheses_counter,
            parentheses_content_concatenation,
            digit_concatenation,
            previous_character,
            operator,
            previous_result,
            result,
            previous_number_evaluation,
            previous_term,
            previous_operator,
            term,
            previous_factor
        )


if __name__ == '__main__':
    main()
