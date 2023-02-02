# Arithmetic Stream Computer

Thoughts process:

1. Because the exercice asked to reduce space and time complexity as much as possible, we decided to not use the trivial
   solution of storing the stream indefinitely and running the `eval()` function on it. Indeed, this would require
   storage and computing capacity of the same order of magnitude as the length of digit stream.
2. In order to reduce the amount of streamed digits we need to store at any time, we can find after which conditions
   we can safely compute intermediate results, store those intermediate results and completely discard the part of the
   stream that comes before.
    1. The first culprits for having to keep some storage of previous results are multiplications/divisions because
       they can change the last term of an addition/subtraction and therefore force us to keep the `previous_term` and
       the `previous_operator` for the new computation. Ex: If the stream is `2 + 3 * 5`, we need to recompute the 
       addition after the multiplication by 5.
    2. As the characters are entered one by one, we need to concatenate the digits of a multi-digit number,
       we do that in `digit_concatenation`.
    3. An operation may take multiple inputs to be possible to compute, and a new input may require a re-computation of
       the `previous_term` of an addition/subtraction, so we need to store everything else (not already mentioned)
       necessary to recompute: current active `operator`, current active `term`, `previous_result`,
       `previous_number_evaluation`, and `previous_factor`.
    4. Finally, if we add parentheses, then we have to consider that the whole parentheses content may be later
       multiplied/divided, so we need to evaluate the content of parentheses first when they are closed and starting
       from the most nested first.
        1. The support for parenthesis is not complete. While the use case from the exercise is covered, and multiple
           others, some specific use cases such as evaluating to a negative value or nested parenthesis are not.
        2. The specific case of having no parentheses can be understood as having only one pair of external parentheses,
           so it's eventually just a specific use case for computing inside parentheses.
        3. Parenthesis lead us to have two additional variables to store the number of opened parentheses which must
           be closed to complete the computation in `opened_parentheses_counter` and a concatenation of the characters
           making the content of the parentheses in `parentheses_content_concatenation`.
3. This complexity of having to keep intermediate results is reflected in the signatures of the main functions created,
   `handle_parentheses()` and `compute_inside_parentheses()`. Their signatures reflect the various intermediate stored
   values.
4. Various forbidden input sequences included the double operator from the exercise are handled using python
   `Exception` and thanks to storing the `previous_character`.

Eventually, as long as the arithmetic terms or the parenthesis content are much smaller than the full stream, which is
expected (otherwise one may question the producer of this stream), this method, while quite complex to write, should
be much more efficient in terms of storage and computation once the stream gets to a significant size.

## Install

Clone the repository.

## Run

This start a small CLI that lets you manually produce a stream of characters.
In case of forbidden entry, an exception will stop the app, you can simply restart it.

```shell
python main.py
```

## Tests

- All the given examples are covered by the tests including the one with parentheses
- 16 additional tests are included to cover other tricky use cases
- 3 tests are left failing to describe use cases not covered: some case of parentheses returning a negative value and
  nested parentheses.

Install testing library:

```shell
pip install pytest
```

Run:

```shell
pytest
```

