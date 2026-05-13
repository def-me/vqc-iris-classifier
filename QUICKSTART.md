# Quick Start Guide

Welcome to the **Variational Quantum Classifier** project! Get up and running in 5 minutes.

## Prerequisites

- **Python 3.8+**
- **pip** or **conda**

## Installation

### Option 1: Direct Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/vqc-iris-classifier.git
cd vqc-iris-classifier

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Install in development mode with extra tools
pip install -e ".[dev]"
```

### Option 2: Using Docker

```bash
# Build and run with Docker
docker-compose build
docker-compose run vqc

# Or start Jupyter notebook
docker-compose up jupyter
# Then navigate to http://localhost:8888
```

### Option 3: Using Poetry

```bash
pip install poetry
poetry install
poetry run python vqc_iris.py
```

## Run Training

### Quick Training (Default Settings)

```bash
python vqc_iris.py
```

This will:
- Load the Iris dataset
- Train for 80 epochs
- Save results to `results/`
- Display training progress

### Using Make Command

```bash
make train
```

### Expected Output

```
======================================================================
🔬 Variational Quantum Classifier (VQC) - Iris Dataset
======================================================================
Backend: PennyLane
Qubits: 4 | Layers: 3 | Trainable Params: 24
======================================================================

📊 Loading Iris dataset...
Classes: 3 | Samples per class: [50 50 50]
Train samples: 90 | Val samples: 30 | Test samples: 30

🚀 Training Variational Quantum Classifier...
Epoch 10/80 | Train Loss: 0.8234 | Val Loss: 0.7891 | Train Acc: 0.7222 | Val Acc: 0.7333
Epoch 20/80 | Train Loss: 0.5123 | Val Loss: 0.4892 | Train Acc: 0.8444 | Val Acc: 0.8667
...

📈 Evaluating model...
✅ Test Accuracy: 0.8333

🎨 Generating visualizations...
✅ Saved training curves to results/training_curves.png
✅ Saved confusion matrix to results/confusion_matrix.png
✅ Saved circuit diagram to results/circuit_diagram.png

======================================================================
✅ Training complete! Results saved to results/
======================================================================
```

## Results

Results are saved in the `results/` directory:

- **training_curves.png** - Loss and accuracy over epochs
- **confusion_matrix.png** - Per-class classification performance
- **circuit_diagram.png** - Quantum circuit visualization
- **metrics.json** - Detailed metrics and hyperparameters

## Interactive Exploration

Explore the VQC implementation in a Jupyter notebook:

```bash
jupyter notebook notebooks/vqc_exploration.ipynb
```

Or use the make command:

```bash
make notebook
```

## Development

### Run Tests

```bash
pytest tests/ -v
# or
make test
```

### Code Quality Checks

```bash
# Format code
make format

# Check code quality
make lint

# All at once
make all
```

### View Available Commands

```bash
make help
```

## Configuration

Modify hyperparameters in `vqc_iris.py`:

```python
N_QUBITS = 4          # Number of qubits
N_LAYERS = 3          # Ansatz layers
LEARNING_RATE = 0.08  # Optimizer learning rate
N_EPOCHS = 80         # Training epochs
BATCH_SIZE = 16       # Batch size
```

## Troubleshooting

### PennyLane Not Available

The code falls back to a pure NumPy simulator automatically. To use PennyLane:

```bash
pip install pennylane
```

### Out of Memory

Reduce `N_QUBITS` or increase Python's available memory:

```bash
export PYTHONHASHSEED=0
python vqc_iris.py
```

### Slow Training

Training with PennyLane on CPU is slower. To speed up:

1. Use NumPy simulator (automatic if PennyLane not available)
2. Reduce `N_QUBITS` from 4 to 2-3
3. Use GPU acceleration if available

## Next Steps

1. **Explore Results**: Check `results/` for visualizations
2. **Read Documentation**: See [README.md](README.md) for theory
3. **Modify Code**: Try different hyperparameters in `vqc_iris.py`
4. **Extend Project**: Add new features or datasets
5. **Contribute**: See [CONTRIBUTING.md](../CONTRIBUTING.md) to contribute

## Key Resources

- **Main Script**: [vqc_iris.py](../vqc_iris.py)
- **Jupyter Notebook**: [vqc_exploration.ipynb](../notebooks/vqc_exploration.ipynb)
- **Full Documentation**: [README.md](../README.md)
- **Contributing Guide**: [CONTRIBUTING.md](../CONTRIBUTING.md)
- **PennyLane Docs**: https://pennylane.ai/

## Common Questions

**Q: What's the expected test accuracy?**
A: ~83.3% on the Iris dataset. Perfect Setosa classification, reasonable Versicolor/Virginica boundary.

**Q: Can I use this on other datasets?**
A: Yes! You'll need to:
   - Normalize features to [−1, 1]
   - Adjust `N_QUBITS` based on number of features
   - Possibly use amplitude encoding for higher dimensions

**Q: How long does training take?**
A: ~2-3 minutes with NumPy, ~12-15 minutes with PennyLane on CPU.

**Q: Can I run this on quantum hardware?**
A: Yes, with PennyLane's hardware backends (IBM Qiskit, IonQ, etc.). See PennyLane documentation.

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/vqc-iris-classifier/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/vqc-iris-classifier/discussions)
- **Email**: your.email@example.com

---

**Ready to train? Run:** `python vqc_iris.py` 🚀
