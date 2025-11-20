Here is the foundational document for the **Aether** project.

---

# The Aether Manifesto
**Version 0.1**
*Toward an Ambient Compute Lattice*

### Preamble
For a decade, we have optimized the **Shipping Container** (Docker/Kubernetes). We treated software like heavy cargo—wrapping it in layers of operating systems, libraries, and security policies, then hiring cranes (Orchestrators) to stack them onto ships (Clusters).

This model has reached its limit. It is heavy, slow, and brittle.

We believe the future of infrastructure is not **Nautical** (shipping containers), but **Quantum** (energy packets). We propose a shift from **managing servers** to **managing intent**.

We call this platform **Aether**.

---

### The Four Laws of Aether

#### 1. The Law of Atomicity: The Particle, Not the OS
**We believe logic should travel without luggage.**
Current containers are 99% Operating System and 1% Application. This is wasteful.
* **In Aether:** The unit of compute is the **Particle** (WebAssembly Component). It contains *only* business logic. It has no shell, no users, and no filesystem.
* **The Shift:** From "Booting Linux" (Seconds) to "Invoking Functions" (Milliseconds).

#### 2. The Law of Locality: The Lattice, Not the Cluster
**We believe boundaries are artificial.**
The concept of a "Cluster" creates silos. It requires complex federation to bridge regions.
* **In Aether:** There is only **The Lattice**. It is a masterless, peer-to-peer mesh (inspired by the Cassandra Ring). A server in Tokyo and a laptop in New York are peers in the same swarm. Capacity is discovered via gossip, not assigned by a master.
* **The Shift:** From "Centralized Control Plane" to "Emergent Swarm Intelligence."

#### 3. The Law of Ambience: The Stream, Not the Proxy
**We believe the network should be invisible.**
Sidecars (Envoy, Linkerd) are a tax on throughput. Applications should not bear the burden of the network stack.
* **In Aether:** Networking is pushed into the kernel via **eBPF**. Security, mTLS, and Observability are properties of the "atmosphere," not the application.
* **The Shift:** From "Service Meshes" to "Kernel-Native Networking."

#### 4. The Law of Continuity: The Pulse, Not the Loop
**We believe software should not have amnesia.**
Reconciliation loops (State A != State B, try again) are fragile. They lose context when they crash.
* **In Aether:** Infrastructure changes are **Durable Workflows**. If a deployment is interrupted, it does not restart; it resumes.
* **The Shift:** From "Eventual Consistency" to "Guaranteed Execution."

---

### The Comparative Value System

While there is value in the items on the right, we value the items on the left more:

| We Value... | Over... |
| :--- | :--- |
| **Instant Ephemerality** | Long-running Processes |
| **Universal API (Wasm)** | Linux System Calls |
| **Global Gossip (Ring)** | Centralized etcd |
| **Strict Types (CUE)** | Text Templates (YAML) |
| **Capabilities** | Permissions |

---

### The Architectural Standard

**1. The Compute Layer: Wasm Components**
We reject the Docker image. We embrace the Wasm Component Model (WASI 0.2) as the universal binary format. It runs anywhere, securely, instantly.

**2. The Network Layer: The Ambient Stream**
We reject the Sidecar. We embrace eBPF to handle L4/L7 traffic at the kernel level, creating a flat, encrypted address space for all Particles.

**3. The Control Layer: The Durable Pulse**
We reject the Polling Loop. We embrace Durable Execution (Temporal-style) to model infrastructure lifecycles as long-running, fault-tolerant code.

**4. The Storage Layer: Disaggregated State**
We reject the Local Disk. We embrace storage-as-a-service. State is external to the Compute.

---

### The End State

When Aether is running, the "Computer" is no longer a specific machine.
**The Lattice is the Computer.**

You push code. It exists everywhere and nowhere. It runs only when needed. It scales with the fluid dynamics of a gas, not the mechanics of a solid.

*Stop steering ships. Become the atmosphere.*

---

### Your Move
This is the high-level vision. To make this real, we need to define the **Developer Experience (DX)**.

Would you like to see the **`Aetherfile`** (the configuration schema) to see how a developer would actually describe a "Particle" in this new world?