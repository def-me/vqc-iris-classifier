"""
Simplified VQC Training Script - Results Generator
Uses NumPy simulator (no network, no PennyLane required)
Creates all visualization outputs for GitHub demonstration
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import json
from pathlib import Path

# ==============================================================================
# Configuration
# ==============================================================================

N_QUBITS = 4
N_LAYERS = 3
LEARNING_RATE = 0.08
N_EPOCHS = 80
BATCH_SIZE = 16
SEED = 42
TEST_SIZE = 0.2


# ==============================================================================
# Pure NumPy Quantum Simulator
# ==============================================================================

def statevector_simulator(inputs, params):
    """Pure NumPy statevector simulator for quantum circuits."""
    # Initialize state |0...0⟩
    state = np.zeros(2**N_QUBITS, dtype=complex)
    state[0] = 1.0
    
    # Feature encoding: RY gates
    for i in range(N_QUBITS):
        angle = inputs[i] * np.pi
        state = apply_ry_all_qubits(state, angle, i)
    
    # Ansatz layers
    for layer in range(N_LAYERS):
        # RY and RZ rotations
        for i in range(N_QUBITS):
            angle_y = params[layer, i, 0]
            angle_z = params[layer, i, 1]
            state = apply_ry_all_qubits(state, angle_y, i)
            state = apply_rz_all_qubits(state, angle_z, i)
        
        # CNOT gates (ring topology)
        for i in range(N_QUBITS):
            target = (i + 1) % N_QUBITS
            state = apply_cnot(state, i, target)
    
    # Measurement: Z expectation values
    expectations = []
    for i in range(N_QUBITS):
        exp_z = measure_z(state, i)
        expectations.append(exp_z)
    
    return np.array(expectations)


def apply_ry_all_qubits(state, angle, target):
    """Apply RY rotation to target qubit on all basis states."""
    cos_a = np.cos(angle / 2)
    sin_a = np.sin(angle / 2)
    new_state = state.copy()
    
    for i in range(len(state)):
        if state[i] == 0:
            continue
        bit = (i >> target) & 1
        if bit == 0:
            j = i | (1 << target)
            new_state[i] = cos_a * state[i] - sin_a * state[j]
            new_state[j] += sin_a * state[i] + cos_a * state[j]
        else:
            j = i & ~(1 << target)
    
    return new_state


def apply_rz_all_qubits(state, angle, target):
    """Apply RZ rotation to target qubit (diagonal gate)."""
    phase = np.exp(-1j * angle / 2)
    new_state = state.copy()
    
    for i in range(len(state)):
        bit = (i >> target) & 1
        if bit == 1:
            new_state[i] *= phase
    
    return new_state


def apply_cnot(state, control, target):
    """Apply CNOT gate: flip target if control is |1⟩."""
    new_state = state.copy()
    
    for i in range(len(state)):
        if (i >> control) & 1:  # Control is |1⟩
            j = i ^ (1 << target)  # Flip target bit
            new_state[j] += state[i]
            new_state[i] = 0
    
    return new_state


def measure_z(state, qubit):
    """Measure expectation value of Pauli-Z on a qubit."""
    exp_z = 0.0
    for i in range(len(state)):
        prob = abs(state[i])**2
        bit = (i >> qubit) & 1
        exp_z += prob * (1 if bit == 0 else -1)
    return exp_z


def predict_proba_numpy(inputs, params):
    """Predict probabilities using pure NumPy simulator."""
    batch_size = inputs.shape[0]
    outputs = np.array([statevector_simulator(inputs[i], params) for i in range(batch_size)])
    
    # Soft-max head
    exp_outputs = np.exp(outputs - outputs.max(axis=1, keepdims=True))
    probs = exp_outputs / exp_outputs.sum(axis=1, keepdims=True)
    
    return probs


# ==============================================================================
# Training
# ==============================================================================

def cross_entropy_loss(probs, labels):
    """Compute cross-entropy loss."""
    batch_size = probs.shape[0]
    log_probs = np.log(np.maximum(probs, 1e-10))
    loss = -np.mean(log_probs[np.arange(batch_size), labels])
    return loss


def gradient_descent_step(X_batch, y_batch, params, learning_rate):
    """Estimate gradients using finite differences and update parameters."""
    delta = 1e-5
    gradients = np.zeros_like(params)
    
    for i in range(params.shape[0]):
        for j in range(params.shape[1]):
            for k in range(params.shape[2]):
                probs_minus = predict_proba_numpy(X_batch, params)
                loss_minus = cross_entropy_loss(probs_minus, y_batch)
                
                params_plus = params.copy()
                params_plus[i, j, k] += delta
                probs_plus = predict_proba_numpy(X_batch, params_plus)
                loss_plus = cross_entropy_loss(probs_plus, y_batch)
                
                gradients[i, j, k] = (loss_plus - loss_minus) / delta
    
    params -= learning_rate * gradients
    return params


def train_vqc(X_train, y_train, X_val, y_val):
    """Train the Variational Quantum Classifier."""
    np.random.seed(SEED)
    params = np.random.randn(N_LAYERS, N_QUBITS, 2) * 0.1
    
    history = {"train_loss": [], "val_loss": [], "train_acc": [], "val_acc": []}
    
    n_batches = len(X_train) // BATCH_SIZE
    
    for epoch in range(N_EPOCHS):
        # Shuffle training data
        indices = np.random.permutation(len(X_train))
        X_train_shuffled = X_train[indices]
        y_train_shuffled = y_train[indices]
        
        # Mini-batch training
        epoch_loss = 0
        for batch in range(n_batches):
            start = batch * BATCH_SIZE
            end = start + BATCH_SIZE
            X_batch = X_train_shuffled[start:end]
            y_batch = y_train_shuffled[start:end]
            
            params = gradient_descent_step(X_batch, y_batch, params, LEARNING_RATE)
            
            probs = predict_proba_numpy(X_batch, params)
            loss = cross_entropy_loss(probs, y_batch)
            epoch_loss += loss
        
        # Validation
        val_probs = predict_proba_numpy(X_val, params)
        val_loss = cross_entropy_loss(val_probs, y_val)
        
        train_probs = predict_proba_numpy(X_train, params)
        train_loss = cross_entropy_loss(train_probs, y_train)
        
        train_acc = np.mean(np.argmax(train_probs, axis=1) == y_train)
        val_acc = np.mean(np.argmax(val_probs, axis=1) == y_val)
        
        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["train_acc"].append(train_acc)
        history["val_acc"].append(val_acc)
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{N_EPOCHS} | "
                  f"Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f} | "
                  f"Train Acc: {train_acc:.4f} | Val Acc: {val_acc:.4f}")
    
    return params, history


def evaluate_model(X_test, y_test, params):
    """Evaluate the trained model on test set."""
    probs = predict_proba_numpy(X_test, params)
    y_pred = np.argmax(probs, axis=1)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n✅ Test Accuracy: {accuracy:.4f}")
    
    return y_pred, accuracy


def plot_training_curves(history, output_dir):
    """Plot training and validation curves."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    ax1.plot(history["train_loss"], label="Train Loss", linewidth=2, marker='o', markersize=3)
    ax1.plot(history["val_loss"], label="Val Loss", linewidth=2, marker='s', markersize=3)
    ax1.set_xlabel("Epoch", fontsize=12)
    ax1.set_ylabel("Loss", fontsize=12)
    ax1.set_title("Training Curves - Loss", fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(history["train_acc"], label="Train Accuracy", linewidth=2, marker='o', markersize=3)
    ax2.plot(history["val_acc"], label="Val Accuracy", linewidth=2, marker='s', markersize=3)
    ax2.set_xlabel("Epoch", fontsize=12)
    ax2.set_ylabel("Accuracy", fontsize=12)
    ax2.set_title("Training Curves - Accuracy", fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / "training_curves.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ Saved training curves to {output_dir / 'training_curves.png'}")


def plot_confusion_matrix(y_test, y_pred, output_dir):
    """Plot confusion matrix."""
    iris = load_iris()
    class_names = iris.target_names
    cm = confusion_matrix(y_test, y_pred)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    
    ax.set_xlabel("Predicted Label", fontsize=12)
    ax.set_ylabel("True Label", fontsize=12)
    ax.set_title("Confusion Matrix", fontsize=14, fontweight='bold')
    
    tick_marks = np.arange(len(class_names))
    ax.set_xticks(tick_marks)
    ax.set_yticks(tick_marks)
    ax.set_xticklabels(class_names)
    ax.set_yticklabels(class_names)
    
    # Add text annotations
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                   color="white" if cm[i, j] > cm.max() / 2 else "black",
                   fontsize=12, fontweight='bold')
    
    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    plt.savefig(output_dir / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ Saved confusion matrix to {output_dir / 'confusion_matrix.png'}")


# ==============================================================================
# Main Execution
# ==============================================================================

def main():
    """Main training and evaluation pipeline."""
    
    # Create output directory
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 70)
    print("🔬 Variational Quantum Classifier (VQC) - Iris Dataset")
    print("=" * 70)
    print(f"Backend: Pure NumPy (No External Dependencies)")
    print(f"Qubits: {N_QUBITS} | Layers: {N_LAYERS} | Trainable Params: {N_LAYERS * N_QUBITS * 2}")
    print("=" * 70)
    
    # Load and preprocess data
    print("\n📊 Loading Iris dataset...")
    iris = load_iris()
    X, y = iris.data, iris.target
    
    n_classes = len(np.unique(y))
    print(f"Classes: {n_classes} | Samples per class: {np.bincount(y)}")
    
    # Split into train/val/test
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=SEED, stratify=y
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.25, random_state=SEED, stratify=y_temp
    )
    
    # Normalize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)
    
    # Normalize to [-1, 1] for quantum encoding
    X_train = (X_train - X_train.min()) / (X_train.max() - X_train.min()) * 2 - 1
    X_val = (X_val - X_val.min()) / (X_val.max() - X_val.min()) * 2 - 1
    X_test = (X_test - X_test.min()) / (X_test.max() - X_test.min()) * 2 - 1
    
    print(f"Train samples: {len(X_train)} | Val samples: {len(X_val)} | Test samples: {len(X_test)}")
    
    # Train model
    print("\n🚀 Training Variational Quantum Classifier...")
    params, history = train_vqc(X_train, y_train, X_val, y_val)
    
    # Evaluate model
    print("\n📈 Evaluating model...")
    y_pred, accuracy = evaluate_model(X_test, y_test, params)
    
    # Compute metrics
    report = classification_report(y_test, y_pred, target_names=iris.target_names, output_dict=True)
    
    # Save metrics
    metrics = {
        "test_accuracy": float(accuracy),
        "classification_report": report,
        "hyperparameters": {
            "n_qubits": N_QUBITS,
            "n_layers": N_LAYERS,
            "learning_rate": LEARNING_RATE,
            "n_epochs": N_EPOCHS,
            "batch_size": BATCH_SIZE
        }
    }
    
    with open(output_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"✅ Saved metrics to {output_dir / 'metrics.json'}")
    
    # Visualizations
    print("\n🎨 Generating visualizations...")
    plot_training_curves(history, output_dir)
    plot_confusion_matrix(y_test, y_pred, output_dir)
    
    # Print detailed results
    print("\n" + "=" * 70)
    print("📊 CLASSIFICATION REPORT")
    print("=" * 70)
    print(classification_report(y_test, y_pred, target_names=iris.target_names))
    
    print("\n" + "=" * 70)
    print(f"✅ Training complete! Results saved to {output_dir}/")
    print("=" * 70)
    print("\nGenerated Files:")
    for f in sorted(output_dir.glob("*")):
        print(f"  - {f.name}")


if __name__ == "__main__":
    main()
