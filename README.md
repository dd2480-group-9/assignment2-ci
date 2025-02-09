# DD2480-group9-lab2-CI

## Usage

### Prerequisites

- **Python 3.13** (no external libraries required)

### Testing

- A **test suite** in `/test` verifies the correctness of each LIC function and the final decision logic.
- Run the tests with:
  ```sh
  python -m unittest discover test
  ```

## Documentation
API documentation is generated automatically with [pdoc](https://github.com/mitmproxy/pdoc) for all modules in `src/` when commits are pushed to main and can be viewed [here](https://dd2480-group-9.github.io/assignment2-ci/).

API documentation can also be generated locally by running
```shell
pip install pdoc
```
and then
```shell
pdoc src/ -d google
```
for more informatino about pdoc see the [documentation](https://pdoc.dev/docs/pdoc.html).

### Docstrings
All docstrings are written following the [google styleguide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings). Specifically, the style guidelines for [modules](https://google.github.io/styleguide/pyguide.html#382-modules), [functions](https://google.github.io/styleguide/pyguide.html#383-functions-and-methods), and [classes](https://google.github.io/styleguide/pyguide.html#384-classes) should be followed to ensure the API documentation is generated correctly.

## Workflow
Throughout the project, issues were created and assigned to all parts of the program, ensuring clarity in development tasks. The goals for the lab were structured into milestones, allowing for systematic progress tracking.

All implementation was done in separate branches, each linked to at least one issue. Before merging any changes into the `main` branch, at least two team members reviewed the modifications to maintain code quality and consistency.

Commits should be structured following the format: `typeprefix(function or file): description #issue`, where `typeprefix` could be one of the following:
- `feat`: Introducing a new feature.
- `fix`: Fixing a bug.
- `test`: Adding or modifying tests.
- `refactor`: Code restructuring or improvements without changing functionality.
- `docs`: Documentation updates.
- `chore`: Miscellaneous commits e.g. modifying .gitignore

`function or file` refers to what part of the code base that is addressed and `#issue` refers to what issue this commit relates to if applicable.
This workflow ensured an organized and efficient development process.

### Statement of contribution
- **Alexandra Ejnervall**: 
- **Eren Özogul**: 
- **Ryll Åman**: API documentation generation and structure.
- **Sebastian Kristoffersson**: 
- **Youngbin Pyo**: 