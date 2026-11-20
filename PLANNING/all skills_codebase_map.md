# 🗺️ UniCortex Dense Holographic Codebase Map
**Project**: `ALL SKILLS` | **Indexed Source Files**: 18

### 📄 `src/uniskill/cli.py`
```kotlin
@app.command()
def status()
@app.command()
def index(
@app.command()
def sync()
@app.command()
def audit()
@app.command("eval")
def eval_cmd(
@app.command()
def upgrade(
@app.command()
def forge(
@app.command("list")
def list_cmd(
@app.command("route")
def route_cmd(
@app.command("run")
def run_cmd(
@app.command("learn")
def learn_cmd(
@app.command("ensure")
def ensure_cmd(
```

### 📄 `src/uniskill/elevate.py`
```kotlin
def calculate_bm25_score(
def audit_delta_gap(
def elevate_skill_to_100_percent(
```

### 📄 `src/uniskill/evaluator.py`
```kotlin
class ProjectStackInspector
def inspect(project_path
def evaluate_skill_for_project(
```

### 📄 `src/uniskill/forge.py`
```kotlin
def verify_capability() -> bool
def synthesize_new_skill(
def test_invariants()
```

### 📄 `src/uniskill/invariants.py`
```kotlin
class InvariantViolation(Exception)
def check_devanagari_invariant(text
def check_vehicle_metaphor_invariant(text
def parse_and_validate_frontmatter(content
def validate_python_syntax(code
def validate_bracket_balance(code
def validate_skill_file(skill_path
```

### 📄 `src/uniskill/learner.py`
```kotlin
def parse_latest_dev_log(project_root
def distill_lesson_into_skill(
```

### 📄 `src/uniskill/registry.py`
```kotlin
def compute_file_sha256(path
def infer_domain_category(skill_name
def infer_compatibility_matrix(skill_name
def index_all_skills(
def get_skill(name
def list_skills(category
def get_catalog_stats(db_path
```

### 📄 `src/uniskill/router.py`
```kotlin
def tokenize(text
def route_skills_for_task(
```

### 📄 `src/uniskill/runner.py`
```kotlin
def list_skill_scripts(skill_name
def run_skill_script(
```

### 📄 `src/uniskill/sync.py`
```kotlin
def audit_triple_env_parity() -> Dict[str, Any]
def sync_skill_to_all_environments(
def sync_all_skills_across_environments(
```

### 📄 `src/uniskill/upgrader.py`
```kotlin
def sanitize_text(text
def format_frontmatter_block_scalar(name
def upgrade_skill_file(
```

### 📄 `tests/test_elevate.py`
```kotlin
class TestElevate(unittest.TestCase)
def setUp(self)
def tearDown(self)
def test_delta_gap_detection(self)
def test_100_percent_elevation(self)
```

### 📄 `tests/test_evaluator.py`
```kotlin
class TestEvaluator(unittest.TestCase)
def setUp(self)
def tearDown(self)
def test_project_stack_inspection(self)
def test_skill_evaluation_pass(self)
def test_nonexistent_skill_synthesize_gate(self)
```

### 📄 `tests/test_forge.py`
```kotlin
class TestForgeAndUpgrader(unittest.TestCase)
def setUp(self)
def tearDown(self)
def test_text_sanitization(self)
def test_synthesize_new_skill(self)
def test_upgrade_skill_file(self)
```

### 📄 `tests/test_invariants.py`
```kotlin
class TestInvariants(unittest.TestCase)
def test_devanagari_detection(self)
def test_vehicle_metaphor_detection(self)
def test_frontmatter_validation(self)
def test_python_syntax_validation(self)
def test_bracket_balance(self)
```

### 📄 `tests/test_registry.py`
```kotlin
class TestRegistry(unittest.TestCase)
def setUp(self)
def tearDown(self)
def test_indexing_and_retrieval(self)
```

### 📄 `tests/test_router_and_runner.py`
```kotlin
class TestRouterAndRunner(unittest.TestCase)
def setUp(self)
def tearDown(self)
def test_tokenization(self)
def test_semantic_routing(self)
def test_script_runner(self)
```

### 📄 `tests/test_sync.py`
```kotlin
class TestSync(unittest.TestCase)
def setUp(self)
def tearDown(self)
def test_sync_and_audit(self)
```

