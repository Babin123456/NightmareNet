Hi maintainers! I've completed the implementation for this issue. 

**ECSoC '26 Label Request:**
Based on the ECSoC '26 points criteria, I am requesting the `ECSoC26`, `Level 3`, and `good-backend` labels for this PR. 
* **Justification for Level 3 / good-backend:** This PR introduces a core architectural feature (multi-model orchestrator using isolated `ProcessPoolExecutor` sub-processes to manage VRAM constraints) and advanced performance analytics (Pareto frontier calculation and degradation curve aggregation). It heavily modifies the core evaluation backend and adds comprehensive unit testing (including Pydantic config validation) for these new components, which aligns perfectly with the Level 3 (Core/Arch/Perf) tier.

Looking forward to your review!
