# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-15

### Added
- Initial release of Variational Quantum Classifier (VQC) for Iris dataset
- PennyLane quantum circuit implementation
  - Feature encoding with angle embedding (RY rotations)
  - Ansatz with RY/RZ rotations and CNOT entanglement
  - Pauli-Z measurement on all qubits
- Pure NumPy fallback simulator (statevector simulation)
- Hybrid classical-quantum training loop
  - Finite-difference gradient estimation
  - Mini-batch stochastic gradient descent
  - Cross-entropy loss
- Comprehensive evaluation metrics
  - Accuracy, precision, recall, F1-score
  - Confusion matrix and classification report
  - Per-class performance analysis
- Visualization tools
  - Training curves (loss and accuracy)
  - Confusion matrix heatmap
  - Quantum circuit diagram
- Full test suite
  - Circuit component tests
  - Data preprocessing tests
  - Model training and evaluation tests
- GitHub Actions CI/CD pipeline
  - Multi-OS and multi-Python version testing
  - Code quality checks (flake8, black, isort)
  - Coverage reporting
- Documentation
  - Comprehensive README with theory and references
  - Contributing guidelines
  - Jupyter notebook for exploration
- Development tools
  - Makefile with common commands
  - setup.py for package installation
  - requirements.txt for dependency management

### Performance
- Achieves ~83.3% test accuracy on Iris dataset
- Perfect classification of Setosa (linearly separable)
- Learns meaningful Versicolor/Virginica boundary
- Training time: ~2s per epoch (NumPy), ~15s per epoch (PennyLane on CPU)

## Future Enhancements (Planned)

### Short Term
- [ ] Support for binary classification mode
- [ ] Alternative embedding schemes (amplitude encoding, IQP)
- [ ] Advanced optimizers (Adam, RMSprop)
- [ ] Quantum noise simulation
- [ ] Parameter initialization strategies

### Medium Term
- [ ] Support for larger datasets (MNIST binary, CIFAR-10)
- [ ] Data re-uploading circuits
- [ ] Quantum feature map analysis
- [ ] Expressibility and entanglement metrics
- [ ] Barren plateau mitigation

### Long Term
- [ ] Hardware implementation (IBM Qiskit, IonQ)
- [ ] Distributed training across quantum processors
- [ ] Federated quantum machine learning
- [ ] Quantum transfer learning
- [ ] Integration with other QML frameworks

## Known Issues

None at this time.

## Compatibility

- Python: 3.8, 3.9, 3.10, 3.11
- PennyLane: >= 0.28.0
- NumPy: >= 1.21.0
- Scikit-learn: >= 1.0.0
- Matplotlib: >= 3.4.0
