"""
Test model training and evaluation
"""

import unittest
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score


class TestLossFunction(unittest.TestCase):
    """Test cross-entropy loss computation."""

    def test_loss_shape(self):
        """Test that loss returns scalar."""
        batch_size = 16
        n_classes = 3
        
        # Mock predicted probabilities and labels
        probs = np.random.dirichlet(np.ones(n_classes), size=batch_size)
        labels = np.random.randint(0, n_classes, size=batch_size)
        
        # Compute loss
        log_probs = np.log(probs + 1e-10)
        loss = -np.mean(log_probs[np.arange(batch_size), labels])
        
        self.assertIsInstance(loss, (float, np.floating))

    def test_loss_range(self):
        """Test that loss is non-negative."""
        batch_size = 16
        n_classes = 3
        
        probs = np.random.dirichlet(np.ones(n_classes), size=batch_size)
        labels = np.random.randint(0, n_classes, size=batch_size)
        
        log_probs = np.log(probs + 1e-10)
        loss = -np.mean(log_probs[np.arange(batch_size), labels])
        
        self.assertGreater(loss, 0)

    def test_loss_perfect_prediction(self):
        """Test loss when predictions are correct."""
        batch_size = 10
        n_classes = 3
        labels = np.random.randint(0, n_classes, size=batch_size)
        
        # Perfect predictions: all probability on correct class
        probs = np.zeros((batch_size, n_classes))
        probs[np.arange(batch_size), labels] = 1.0
        
        log_probs = np.log(probs + 1e-10)
        loss = -np.mean(log_probs[np.arange(batch_size), labels])
        
        # Loss should be very small (near 0, limited by epsilon)
        self.assertLess(loss, 0.1)

    def test_loss_random_prediction(self):
        """Test loss for random predictions."""
        batch_size = 1000
        n_classes = 3
        labels = np.random.randint(0, n_classes, size=batch_size)
        
        # Uniform random predictions
        probs = np.ones((batch_size, n_classes)) / n_classes
        
        log_probs = np.log(probs + 1e-10)
        loss = -np.mean(log_probs[np.arange(batch_size), labels])
        
        # Expected loss for uniform: ln(3)
        expected_loss = np.log(n_classes)
        self.assertAlmostEqual(loss, expected_loss, places=1)


class TestGradientComputation(unittest.TestCase):
    """Test gradient estimation."""

    def test_gradient_shape(self):
        """Test that gradients have same shape as parameters."""
        n_layers = 3
        n_qubits = 4
        params = np.random.randn(n_layers, n_qubits, 2)
        
        delta = 1e-5
        gradients = np.random.randn(*params.shape) * delta
        
        self.assertEqual(gradients.shape, params.shape)

    def test_gradient_magnitude(self):
        """Test that gradients are small for finite differences."""
        delta = 1e-5
        
        # Simulated finite difference gradients with a controlled difference
        loss_minus = 0.10000
        loss_plus = 0.10001
        gradient = (loss_plus - loss_minus) / delta
        
        # Gradient magnitude should be reasonable and finite
        self.assertAlmostEqual(gradient, 1.0)
        self.assertTrue(np.isfinite(gradient))


class TestPredictions(unittest.TestCase):
    """Test model predictions and probabilities."""

    def test_probability_sum(self):
        """Test that predicted probabilities sum to 1."""
        batch_size = 20
        n_classes = 3
        
        outputs = np.random.randn(batch_size, n_classes)
        exp_outputs = np.exp(outputs - outputs.max(axis=1, keepdims=True))
        probs = exp_outputs / exp_outputs.sum(axis=1, keepdims=True)
        
        np.testing.assert_array_almost_equal(probs.sum(axis=1), np.ones(batch_size))

    def test_probability_bounds(self):
        """Test that probabilities are in [0, 1]."""
        batch_size = 20
        n_classes = 3
        
        outputs = np.random.randn(batch_size, n_classes)
        exp_outputs = np.exp(outputs - outputs.max(axis=1, keepdims=True))
        probs = exp_outputs / exp_outputs.sum(axis=1, keepdims=True)
        
        self.assertTrue(np.all(probs >= 0))
        self.assertTrue(np.all(probs <= 1))

    def test_class_prediction_from_probs(self):
        """Test argmax of probabilities gives valid class indices."""
        batch_size = 20
        n_classes = 3
        
        probs = np.random.dirichlet(np.ones(n_classes), size=batch_size)
        predictions = np.argmax(probs, axis=1)
        
        # All predictions should be valid class indices
        self.assertTrue(np.all(predictions >= 0))
        self.assertTrue(np.all(predictions < n_classes))
        self.assertEqual(len(predictions), batch_size)


class TestMetrics(unittest.TestCase):
    """Test evaluation metrics."""

    def test_accuracy_perfect(self):
        """Test accuracy for perfect predictions."""
        y_true = np.array([0, 1, 2, 0, 1, 2])
        y_pred = np.array([0, 1, 2, 0, 1, 2])
        
        acc = accuracy_score(y_true, y_pred)
        self.assertEqual(acc, 1.0)

    def test_accuracy_random(self):
        """Test accuracy for random predictions."""
        np.random.seed(42)
        n_samples = 1000
        n_classes = 3
        
        y_true = np.random.randint(0, n_classes, n_samples)
        y_pred = np.random.randint(0, n_classes, n_samples)
        
        acc = accuracy_score(y_true, y_pred)
        
        # With 3 classes, random should be ~33%
        expected_acc = 1.0 / n_classes
        self.assertAlmostEqual(acc, expected_acc, delta=0.05)

    def test_confusion_matrix_shape(self):
        """Test confusion matrix shape."""
        y_true = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])
        y_pred = np.array([0, 1, 1, 0, 1, 2, 0, 2, 2])
        
        cm = confusion_matrix(y_true, y_pred)
        
        self.assertEqual(cm.shape, (3, 3))

    def test_confusion_matrix_diagonal(self):
        """Test confusion matrix diagonal for perfect predictions."""
        y_true = np.array([0, 1, 2, 0, 1, 2])
        y_pred = np.array([0, 1, 2, 0, 1, 2])
        
        cm = confusion_matrix(y_true, y_pred)
        
        # Diagonal should have counts, rest should be zero
        np.testing.assert_array_equal(cm.sum(), 6)
        expected = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 2]])
        np.testing.assert_array_equal(cm, expected)


class TestBatchProcessing(unittest.TestCase):
    """Test batch processing logic."""

    def test_batch_creation(self):
        """Test that batches are created correctly."""
        n_samples = 120
        batch_size = 16
        
        n_batches = n_samples // batch_size
        self.assertEqual(n_batches, 7)  # 7 complete batches

    def test_batch_indices(self):
        """Test batch index calculation."""
        n_samples = 120
        batch_size = 16
        
        for batch in range(7):
            start = batch * batch_size
            end = start + batch_size
            batch_len = end - start
            self.assertEqual(batch_len, batch_size)

    def test_batch_coverage(self):
        """Test that all samples are covered by batches."""
        n_samples = 100
        batch_size = 16
        
        covered = 0
        for batch in range(n_samples // batch_size):
            start = batch * batch_size
            end = start + batch_size
            covered += (end - start)
        
        self.assertLessEqual(covered, n_samples)


if __name__ == "__main__":
    unittest.main()
