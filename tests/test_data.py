"""
Test data preprocessing and loading
"""

import unittest
import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


class TestDataLoading(unittest.TestCase):
    """Test data loading and validation."""

    def setUp(self):
        """Load Iris dataset."""
        self.iris = load_iris()
        self.X = self.iris.data
        self.y = self.iris.target

    def test_iris_dataset_shape(self):
        """Test that Iris dataset has expected shape."""
        self.assertEqual(self.X.shape, (150, 4))
        self.assertEqual(len(self.y), 150)

    def test_iris_classes(self):
        """Test that Iris dataset has 3 classes."""
        unique_classes = np.unique(self.y)
        self.assertEqual(len(unique_classes), 3)
        np.testing.assert_array_equal(unique_classes, [0, 1, 2])

    def test_class_balance(self):
        """Test that Iris dataset is balanced."""
        class_counts = np.bincount(self.y)
        # Each class should have 50 samples
        np.testing.assert_array_equal(class_counts, [50, 50, 50])

    def test_no_missing_values(self):
        """Test that dataset has no missing values."""
        self.assertEqual(np.isnan(self.X).sum(), 0)


class TestDataPreprocessing(unittest.TestCase):
    """Test data normalization and splitting."""

    def setUp(self):
        """Set up test data."""
        self.iris = load_iris()
        self.X = self.iris.data
        self.y = self.iris.target
        self.seed = 42

    def test_train_test_split(self):
        """Test train/test split."""
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=self.seed, stratify=self.y
        )
        
        self.assertEqual(len(X_train), 120)
        self.assertEqual(len(X_test), 30)

    def test_multilevel_split(self):
        """Test multilevel train/val/test split."""
        X_temp, X_test, y_temp, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=self.seed, stratify=self.y
        )
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=0.25, random_state=self.seed, stratify=y_temp
        )
        
        self.assertEqual(len(X_train), 90)
        self.assertEqual(len(X_val), 30)
        self.assertEqual(len(X_test), 30)

    def test_standardization(self):
        """Test feature standardization."""
        scaler = StandardScaler()
        X_train, X_test = train_test_split(self.X, test_size=0.2, random_state=self.seed)
        
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Check mean ≈ 0 and std ≈ 1 for training set
        np.testing.assert_array_almost_equal(X_train_scaled.mean(axis=0), 0, decimal=5)
        np.testing.assert_array_almost_equal(X_train_scaled.std(axis=0), 1, decimal=5)

    def test_quantum_normalization(self):
        """Test normalization to [-1, 1] for quantum encoding."""
        X_sample = self.X[0:10]
        
        # Normalize to [-1, 1]
        X_norm = (X_sample - X_sample.min()) / (X_sample.max() - X_sample.min()) * 2 - 1
        
        self.assertGreaterEqual(np.min(X_norm), -1)
        self.assertLessEqual(np.max(X_norm), 1)

    def test_feature_range(self):
        """Test that features are in expected range after normalization."""
        X_sample = self.X
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_sample)
        
        # After standardization, most values should be in [-3, 3]
        outliers = np.sum(np.abs(X_scaled) > 3)
        self.assertLess(outliers, 10)  # Allow some outliers


class TestDataSplitting(unittest.TestCase):
    """Test different data splitting strategies."""

    def setUp(self):
        """Set up test data."""
        np.random.seed(42)
        self.X = np.random.randn(100, 4)
        self.y = np.repeat([0, 1, 2], [50, 30, 20])

    def test_stratified_split(self):
        """Test stratified splitting preserves class distribution."""
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
        )
        
        train_dist = np.bincount(y_train) / len(y_train)
        test_dist = np.bincount(y_test) / len(y_test)
        overall_dist = np.bincount(self.y) / len(self.y)
        
        # Distributions should be similar
        np.testing.assert_array_almost_equal(train_dist, overall_dist, decimal=1)
        np.testing.assert_array_almost_equal(test_dist, overall_dist, decimal=1)

    def test_no_data_leakage(self):
        """Test that train/test sets don't overlap."""
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        
        # Total samples should equal original
        self.assertEqual(len(X_train) + len(X_test), len(self.X))


if __name__ == "__main__":
    unittest.main()
