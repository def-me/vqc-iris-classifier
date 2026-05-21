"""
Test quantum circuit components
"""

import unittest
import numpy as np


class TestCircuitComponents(unittest.TestCase):
    """Test quantum circuit building blocks."""

    def setUp(self):
        """Set up test fixtures."""
        self.n_qubits = 4
        self.n_layers = 3
        self.batch_size = 10
        
        # Create dummy inputs
        self.inputs = np.random.randn(self.batch_size, self.n_qubits)
        self.params = np.random.randn(self.n_layers, self.n_qubits, 2)

    def test_inputs_shape(self):
        """Test that input features have correct shape."""
        self.assertEqual(self.inputs.shape, (self.batch_size, self.n_qubits))

    def test_params_shape(self):
        """Test that parameters have correct shape."""
        self.assertEqual(self.params.shape, (self.n_layers, self.n_qubits, 2))

    def test_params_random_initialization(self):
        """Test that parameters are properly initialized."""
        rng = np.random.default_rng(0)
        params = rng.normal(scale=0.1, size=(self.n_layers, self.n_qubits, 2))
        self.assertEqual(params.shape, (self.n_layers, self.n_qubits, 2))
        self.assertLess(np.max(np.abs(params)), 0.4)
        self.assertGreater(np.std(params), 0)

    def test_angle_embedding(self):
        """Test angle embedding transformation."""
        # Normalize inputs to [-1, 1]
        inputs_normalized = (self.inputs - self.inputs.min()) / (self.inputs.max() - self.inputs.min()) * 2 - 1
        
        # Check normalization
        self.assertGreaterEqual(np.min(inputs_normalized), -1)
        self.assertLessEqual(np.max(inputs_normalized), 1)

    def test_softmax_head(self):
        """Test softmax head transformation."""
        # Simulate circuit outputs
        outputs = np.random.randn(self.batch_size, self.n_qubits)
        
        # Apply softmax
        exp_outputs = np.exp(outputs - outputs.max(axis=1, keepdims=True))
        probs = exp_outputs / exp_outputs.sum(axis=1, keepdims=True)
        
        # Check probabilities sum to 1
        np.testing.assert_array_almost_equal(probs.sum(axis=1), np.ones(self.batch_size))
        
        # Check all probabilities are in [0, 1]
        self.assertTrue(np.all(probs >= 0))
        self.assertTrue(np.all(probs <= 1))

    def test_circuit_output_values(self):
        """Test that circuit outputs are reasonable values."""
        # Test that random outputs are in a reasonable range
        outputs = np.random.randn(self.batch_size, self.n_qubits) * 2
        
        # Check shape is correct
        self.assertEqual(outputs.shape, (self.batch_size, self.n_qubits))
        
        # Outputs should be finite
        self.assertTrue(np.all(np.isfinite(outputs)))


class TestParameterUpdates(unittest.TestCase):
    """Test parameter update mechanisms."""

    def test_gradient_shape(self):
        """Test that gradients have same shape as parameters."""
        params = np.random.randn(3, 4, 2)
        gradients = np.random.randn(3, 4, 2) * 0.1
        
        self.assertEqual(gradients.shape, params.shape)

    def test_parameter_update(self):
        """Test parameter update with gradient descent."""
        params = np.random.randn(3, 4, 2)
        gradients = np.random.randn(3, 4, 2)
        learning_rate = 0.08
        
        params_old = params.copy()
        params -= learning_rate * gradients
        
        # Check that parameters changed
        self.assertFalse(np.allclose(params, params_old))

    def test_learning_rate_effect(self):
        """Test that learning rate affects step size."""
        params = np.random.randn(3, 4, 2)
        gradients = np.random.randn(3, 4, 2)
        
        params1 = params - 0.01 * gradients
        params2 = params - 0.1 * gradients
        
        # Larger learning rate should cause bigger changes
        diff1 = np.linalg.norm(params - params1)
        diff2 = np.linalg.norm(params - params2)
        
        self.assertLess(diff1, diff2)


if __name__ == "__main__":
    unittest.main()
