import numpy as np
import matplotlib.pyplot as plt

# Data
hours_studied = np.array([1, 3, 4, 6, 7])
exam_scores = np.array([52, 56, 60, 70, 72])

# Calculate coefficients for the regression line
beta_1 = np.corrcoef(hours_studied, exam_scores)[0, 1] * (np.std(exam_scores) / np.std(hours_studied))
beta_0 = np.mean(exam_scores) - beta_1 * np.mean(hours_studied)

# Predict scores using the regression line
predicted_scores = beta_0 + beta_1 * hours_studied

# Plotting
plt.scatter(hours_studied, exam_scores, color='blue', label='Actual Scores')
plt.plot(hours_studied, predicted_scores, color='red', label=f'Regression Line: y = {beta_0:.2f} + {beta_1:.2f}x')
plt.title('Hours Studied vs. Exam Score')
plt.xlabel('Hours Studied')
plt.ylabel('Exam Score')
plt.legend()
plt.grid(True)
plt.show()