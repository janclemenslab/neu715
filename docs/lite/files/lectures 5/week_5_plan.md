# Week 5 — regression

Materials are organized by topic. Lectures and exercises may span sessions.

| Day | Teaching and practice |
| --- | --- |
| Monday | Linear regression: models, slope and intercept, predictions, residuals, least squares, and R². Start Exercise 1: fit and interpret lines for two datasets. Assignment 1 is due, as scheduled in the Week 4 plan. |
| Tuesday | Finish the linear-regression exercises: fit one line per animal, collect and visualize parameters, and compare control and treatment slopes using the statistical methods from Week 4. |
| Wednesday | Nonlinear regression: define an exponential model function, interpret gain and time constant, and fit with `curve_fit`. Keep the embedded sinusoidal-model mini-exercise. Start the quadratic fitting exercise if time permits. |
| Thursday | Finish the nonlinear exercises, including repairing the exponential fit by choosing sensible starting values. Inspect fitted curves and residuals; consolidate parameter interpretation and reporting. Optional parameter bounds and further quadratic practice can fill remaining time. |

## Topic materials

1. [5.01_linear_regression.ipynb](5.01_linear_regression.ipynb) and
   [matching exercises](../exercises%205/5.01_linear_regression_exercises.ipynb):
   fitting and interpreting a line, residuals, MSE and R², and comparing fitted
   parameters across animals.
2. [5.02_nonlinear_regression.ipynb](5.02_nonlinear_regression.ipynb) and
   [matching exercises](../exercises%205/5.02_nonlinear_regression_exercises.ipynb):
   model functions, exponential decay, starting values, quadratic fitting, and
   optional parameter bounds. The sinusoidal mini-exercise remains in the lecture.

## Learning goals

After Week 5, students should be able to:

- distinguish observations, predictions, and fitted parameters;
- fit a line, interpret slope and intercept with units, and plot the predictions;
- calculate residuals and R² and recognize systematic errors in a fitted curve;
- fit one curve per animal and compare parameters at the animal level;
- define a model function for `curve_fit` and keep parameter order consistent;
- interpret exponential gain and time constant and choose plausible starting values;
- explain the difference between interpolation and extrapolation; and
- report fitted parameters and goodness of fit in a short results paragraph.

The core is linear regression, the per-animal comparison, and exponential
fitting. If more practice is needed, give these priority over the quadratic
exercise and optional bounds. There is no pandas/connectomics block.

End with a short check: interpret a slope with units, calculate one prediction
and residual, explain a residual pattern, and identify the independent sample
size in the animal exercise.

## Using the notebooks

Keep the two lecture notebooks with their adjacent `.npz` files and `fig/`
folder. Keep the two exercise notebooks with their four adjacent `.npz` files.
The original datasets and figures are unchanged. The original notebook order,
examples, embedded exercises, and existing worked code are retained, with
targeted corrections. Unfinished answer cells remain for students to complete.

## Downloads

- [Lecture notebooks, data, figures, and week plan](week_5_lectures.zip)
- [Exercise notebooks and data](../exercises%205/week_5_exercises.zip)

Extract each ZIP into a folder before opening its notebooks. The notebooks and data are also included in the browser environment.
