<!--
SYNC IMPACT REPORT
==================
Version change: 1.0.0 → 2.0.0

Modified principles:
- Principle I: Expanded from single-phase to multi-phase evolution (Phase I-V)
- Principle IV: Expanded from in-memory only to full-stack, cloud-native, event-driven architecture
- Technology Standards: Expanded from Python-only to multi-stack (Python, Next.js, FastAPI, Kubernetes, Kafka, Dapr)

Added sections:
- Phase I-V breakdown with specific objectives and tech stacks
- API security principles (JWT, Better Auth)
- Monorepo organization guidelines
- Event-driven architecture principles (Kafka, Dapr)
- Cloud deployment standards (Kubernetes, Helm, Minikube, AKS/GKE)
- AIOps integration (Docker AI/Gordon, kubectl-ai, kagent)
- MCP Server architecture principles
- Stateless design principles

Removed sections: None

Templates requiring updates:
✅ plan-template.md - Compatible with multi-phase architecture
✅ spec-template.md - User story prioritization aligns with incremental delivery
✅ tasks-template.md - Phase-based task organization supports evolution model
✅ phr-template.prompt.md - No changes needed

Follow-up TODOs: None
-->

# Todo App Evolution: From CLI to Cloud-Native AI System Constitution

**Project**: The Evolution of Todo
**Focus**: From CLI to Distributed Cloud-Native AI Systems
**Goal**: Product Architects building progressively complex software using AI without writing boilerplate code

## Project Overview

This constitution governs the development of a Todo application that evolves through five phases, simulating real-world software evolution from a simple script to a Kubernetes-managed, event-driven, AI-powered distributed system.

## Core Principles

### I. Spec-Driven Development (SDD) Across All Phases

Every feature in every phase MUST be developed using the Spec-Driven Development methodology. The workflow is strictly enforced: write specification → generate plan → break into tasks → implement via Claude Code. No feature development begins without a complete specification and plan. Specifications MUST include user stories with priorities (P1, P2, P3...), functional requirements, acceptance scenarios, and success criteria.

This principle applies uniformly across all five phases:
- **Phase I**: Simple console app specs
- **Phase II**: Full-stack web application specs with API contracts
- **Phase III**: AI chatbot specs with MCP tool definitions
- **Phase IV**: Kubernetes deployment specs with Helm charts
- **Phase V**: Event-driven distributed system specs with Kafka and Dapr

The Spec-Driven approach ensures all requirements are understood before any code is written, enabling effective use of Claude Code for implementation.

### II. Agentic Implementation

All code implementation MUST be performed by Claude Code using Spec-Kit Plus tools. Manual coding is strictly prohibited. The implementation follows the Red-Green-Refactor cycle: write failing tests first (Red), implement to make tests pass (Green), then improve code while maintaining functionality (Refactor).

This ensures:
- Consistent code quality across all phases
- Complete automation of boilerplate generation
- Reproducible development process
- Transparent iteration tracking for evaluation

All prompts and iterations are recorded in Prompt History Records (PHRs) for process review and evaluation. Students act as Product Architects, using AI to build rather than coding manually.

### III. Incremental Delivery & Phase Evolution

Features and phases are delivered incrementally with validation at each checkpoint. Each phase builds upon the previous phase while maintaining backward compatibility where applicable.

**Phase Progression**:
1. **Phase I**: In-memory console app (Basic Level: 5 CRUD operations)
2. **Phase II**: Full-stack web app with persistent storage (Basic Level + Authentication)
3. **Phase III**: AI chatbot with MCP server (Natural language interface)
4. **Phase IV**: Local Kubernetes deployment (Containerization + orchestration)
5. **Phase V**: Cloud-native distributed system (Advanced features + event-driven architecture)

**Validation Requirements**:
- Each phase MUST be fully functional before proceeding to the next
- Features within a phase are delivered by priority (P1 → P2 → P3)
- Higher priority user stories are implemented first
- Implementation stops after each priority level for validation
- No lower priority features are started until higher priority features are complete and tested

### IV. Progressive Complexity with Justification

The architecture evolves from simple to complex across phases, with each increase in complexity explicitly justified by new requirements.

**Complexity Evolution**:
- **Phase I**: In-memory storage (lists, dicts) - minimal complexity
- **Phase II**: Database persistence (Neon PostgreSQL), REST API, authentication - justified by multi-user requirements
- **Phase III**: AI agents, MCP servers, stateless architecture - justified by natural language interface requirements
- **Phase IV**: Containers, Kubernetes, Helm charts - justified by deployment scalability requirements
- **Phase V**: Event-driven (Kafka), distributed runtime (Dapr), microservices - justified by advanced features (recurring tasks, reminders, real-time sync)

Any complexity introduced MUST be documented in the Complexity Tracking section of implementation plans, with explicit justification for why simpler alternatives are insufficient.

**Prohibited**: Adding complexity for "future-proofing" or "best practices" without clear current requirements driving the need.

### V. Clean Code & Testing Discipline

Code MUST follow language-specific best practices and clean code principles across all phases:

**Python (Phases I-V backend)**:
- Type hints MANDATORY for all function signatures
- PEP 8 style guide enforced by linting tools
- Docstrings REQUIRED for all public functions, classes, modules
- Small functions with single responsibility
- Descriptive names that reveal intent

**TypeScript/JavaScript (Phases II-V frontend)**:
- TypeScript for type safety
- ESLint and Prettier for consistency
- Component-based architecture with clear separation of concerns
- Server components by default, client components only when needed

**Testing Requirements**:
- Tests MUST be written before implementation (Red-Green-Refactor)
- Unit tests MUST be fast, isolated, and deterministic
- Integration tests MUST validate cross-component interactions
- Contract tests MUST validate API contracts (Phases II-V)
- Tests MUST run and pass before committing changes

**Error Handling**:
- Errors MUST be caught and handled gracefully
- User-facing error messages MUST be clear and actionable
- Internal errors MUST be logged with sufficient context

## Technology Standards

### Phase I: In-Memory Console App

**Stack**:
- Python 3.13+ (runtime)
- UV (package manager)
- Standard library only (no external dependencies)
- In-memory storage (Python data structures: lists, dicts)

**Tools**:
- Claude Code + Spec-Kit Plus (development)
- pytest (testing)
- Ruff (linting and formatting)
- pyright or mypy (type checking)

**Project Structure**:
```
src/
├── models/       # Data models
├── services/     # Business logic
├── cli/          # Command-line interface
└── lib/          # Utilities

tests/
├── unit/         # Unit tests
└── integration/  # Integration tests
```

**WSL 2 Requirement**: Windows users MUST use WSL 2 (Windows Subsystem for Linux) for development environment.

### Phase II: Full-Stack Web Application

**Stack**:
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens
- **Spec-Driven**: Claude Code + Spec-Kit Plus

**Architecture Pattern**: Monorepo with separate frontend and backend directories

**API Security**:
- JWT tokens issued by Better Auth on frontend
- Backend verifies JWT signature using shared secret (BETTER_AUTH_SECRET)
- All API endpoints require valid JWT in Authorization: Bearer <token> header
- Backend filters all queries by authenticated user ID
- User isolation enforced at API level

**Project Structure**:
```
frontend/
├── src/
│   ├── app/          # Next.js pages (App Router)
│   ├── components/   # React components
│   ├── lib/          # API client, utilities
│   └── styles/       # Tailwind CSS
├── CLAUDE.md         # Frontend-specific instructions
└── package.json

backend/
├── src/
│   ├── main.py       # FastAPI entry point
│   ├── models.py     # SQLModel models
│   ├── routes/       # API route handlers
│   └── db.py         # Database connection
├── CLAUDE.md         # Backend-specific instructions
└── pyproject.toml

.specify/             # Spec-Kit Plus configuration
specs/                # Specifications organized by type
CLAUDE.md             # Root instructions
README.md
docker-compose.yml
```

**Monorepo Benefits**:
- Single context for Claude Code (sees entire project)
- Easier cross-cutting changes
- Unified specification management
- Simpler deployment coordination

### Phase III: AI Chatbot with MCP Server

**Stack**:
- **Frontend**: OpenAI ChatKit
- **Backend**: Python FastAPI
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK (Python)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL (with conversation state)
- **Authentication**: Better Auth with JWT

**Architecture Principles**:
- **Stateless Server**: All conversation state persisted to database
- **Scalable**: Any server instance can handle any request
- **Resilient**: Server restarts don't lose conversation state
- **Horizontal Scaling**: Load balancer can route to any backend

**MCP Tools** (exposed by MCP server):
- add_task(user_id, title, description)
- list_tasks(user_id, status)
- complete_task(user_id, task_id)
- delete_task(user_id, task_id)
- update_task(user_id, task_id, title, description)

**Database Models**:
- Task: user_id, id, title, description, completed, created_at, updated_at
- Conversation: user_id, id, created_at, updated_at
- Message: user_id, id, conversation_id, role, content, created_at

**Request Flow**:
1. Receive user message
2. Fetch conversation history from database
3. Build message array for agent (history + new message)
4. Store user message in database
5. Run agent with MCP tools
6. Agent invokes appropriate MCP tool(s)
7. Store assistant response in database
8. Return response to client
9. Server holds NO state (ready for next request)

**OpenAI ChatKit Requirements**:
- Domain allowlist configuration required for hosted deployment
- Domain key from OpenAI security settings
- Localhost works without configuration for local development

### Phase IV: Local Kubernetes Deployment

**Stack**:
- **Containerization**: Docker (Docker Desktop)
- **Docker AI**: Docker AI Agent (Gordon) - AI-assisted Docker operations
- **Orchestration**: Kubernetes (Minikube for local)
- **Package Manager**: Helm Charts
- **AI DevOps**: kubectl-ai, kagent - AI-assisted Kubernetes operations
- **Application**: Phase III Todo Chatbot (containerized)

**Requirements**:
- Containerize frontend and backend applications
- Use Docker AI Agent (Gordon) for intelligent Docker operations
- Create Helm charts for deployment
- Use kubectl-ai and kagent for intelligent Kubernetes operations
- Deploy on Minikube locally

**AIOps Integration**:
- **Gordon**: Docker AI agent for container operations
  - Enable in Docker Desktop 4.53+ (Settings > Beta features)
  - Use for intelligent container builds, optimization, debugging
- **kubectl-ai**: Natural language Kubernetes operations
  - Example: "deploy the todo frontend with 2 replicas"
- **kagent**: Advanced cluster management and optimization
  - Example: "analyze the cluster health"

**Helm Chart Structure**:
```
charts/
├── todo-frontend/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── ingress.yaml
└── todo-backend/
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
        ├── deployment.yaml
        ├── service.yaml
        └── configmap.yaml
```

**Deployment Process**:
1. Containerize applications (using Gordon)
2. Create Helm charts (using kubectl-ai/kagent)
3. Start Minikube cluster
4. Deploy using Helm
5. Validate deployment
6. Test application

### Phase V: Cloud-Native Distributed System

**Stack**:
- **Kubernetes**: Azure AKS / Google Cloud GKE / Oracle OKE
- **Event Streaming**: Kafka (Strimzi self-hosted or Redpanda Cloud)
- **Distributed Runtime**: Dapr (sidecar pattern)
- **CI/CD**: GitHub Actions
- **Monitoring**: Cloud-native observability tools

**Part A: Advanced Features**:
- **Advanced Level**: Recurring Tasks, Due Dates & Reminders
- **Intermediate Level**: Priorities, Tags, Search, Filter, Sort
- Event-driven architecture with Kafka
- Distributed application runtime with Dapr

**Part B: Local Deployment**:
- Deploy to Minikube
- Deploy Dapr on Minikube (Pub/Sub, State, Bindings, Secrets, Service Invocation)

**Part C: Cloud Deployment**:
- Deploy to Azure AKS / Google Cloud GKE / Oracle OKE
- Deploy Dapr on cloud Kubernetes
- Use Kafka on Confluent/Redpanda Cloud or self-hosted (Strimzi)
- Set up CI/CD pipeline (GitHub Actions)
- Configure monitoring and logging

**Event-Driven Architecture (Kafka Use Cases)**:

1. **Reminder/Notification System**:
   - Todo Service publishes reminder events to "reminders" topic
   - Notification Service consumes and sends reminders at due time

2. **Recurring Task Engine**:
   - Task completion event published to "task-events" topic
   - Recurring Task Service consumes and auto-creates next occurrence

3. **Activity/Audit Log**:
   - All task operations published to "task-events" topic
   - Audit Service consumes and maintains complete history

4. **Real-time Sync Across Clients**:
   - Task changes published to "task-updates" topic
   - WebSocket Service consumes and broadcasts to all connected clients

**Kafka Topics**:
- `task-events`: All task CRUD operations (produced by Chat API, consumed by Recurring Task Service, Audit Service)
- `reminders`: Scheduled reminder triggers (produced by Chat API, consumed by Notification Service)
- `task-updates`: Real-time client sync (produced by Chat API, consumed by WebSocket Service)

**Dapr Building Blocks**:

1. **Pub/Sub**: Kafka abstraction - publish/subscribe without Kafka client code
   - App talks to Dapr via HTTP (no kafka-python library needed)
   - Swap Kafka for RabbitMQ with config change, no code changes

2. **State Management**: Conversation state storage
   - Alternative to direct DB calls
   - Store/retrieve state via Dapr HTTP API

3. **Service Invocation**: Frontend → Backend communication
   - Built-in service discovery, retries, mTLS
   - Automatic discovery via Dapr sidecar

4. **Dapr Jobs API**: Scheduled reminders at exact time
   - Schedule reminder at exact datetime (no polling overhead)
   - Callback fires at scheduled time
   - Better than cron bindings (exact timing, scales better)

5. **Secrets Management**: API keys, DB credentials
   - Kubernetes Secrets integration
   - Secure access via Dapr HTTP API

**Architecture Benefits**:
- **Without Dapr**: Direct dependencies (kafka-python, psycopg2), tight coupling, manual retry logic
- **With Dapr**: Single HTTP API, loose coupling, built-in retries, service discovery, vendor independence

**Kafka Recommendations**:
- **Local (Minikube)**: Redpanda Docker container or Strimzi operator
- **Cloud**: Redpanda Cloud Serverless (free tier) or Strimzi self-hosted
- **Justification**: Dapr PubSub makes Kafka-swappable - same APIs, clients work unchanged

**Cloud Provider Options**:
- **Azure AKS**: $200 credits for 30 days
- **Google Cloud GKE**: $300 credits for 90 days
- **Oracle OKE**: Always Free tier (4 OCPUs, 24GB RAM) - Recommended for learning

## Development Workflow

### Spec-Driven Development Lifecycle (All Phases)

1. **Specification**: Create feature spec with user stories (prioritized P1, P2, P3...), requirements, acceptance criteria
2. **Planning**: Generate implementation plan with architecture, data models, contracts, and phase-specific considerations
3. **Task Breakdown**: Create dependency-ordered tasks grouped by user story and phase
4. **Implementation**: Execute tasks via Claude Code following Red-Green-Refactor
5. **Validation**: Test each user story independently before proceeding to next priority
6. **Phase Completion**: Validate entire phase before proceeding to next phase

### Prompt History Records (PHR)

Every user interaction MUST be recorded in a Prompt History Record (PHR). PHRs capture:
- Full user input (verbatim, no truncation)
- Assistant response summary
- Files created/modified
- Tests run/added
- Outcome and evaluation notes
- Phase context (which phase is being worked on)

PHRs are routed to:
- `history/prompts/constitution/` - Constitution-related prompts
- `history/prompts/<feature-name>/` - Feature-specific prompts (includes phase identifier)
- `history/prompts/general/` - General development prompts

### Architectural Decision Records (ADR)

When significant architectural decisions are made (typically during planning and sometimes tasks), run the three-part test:
1. **Impact**: Long-term consequences? (e.g., framework, data model, API, security, platform)
2. **Alternatives**: Multiple viable options considered?
3. **Scope**: Cross-cutting and influences system design?

If ALL true, suggest:
"📋 Architectural decision detected: [brief description] — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"

Wait for user consent; never auto-create ADRs. Group related decisions into one ADR when appropriate.

**Examples of ADR-worthy decisions**:
- Choosing Neon PostgreSQL over local PostgreSQL (Phase II)
- Selecting OpenAI Agents SDK vs custom agent implementation (Phase III)
- Choosing Dapr over direct Kafka clients (Phase V)
- Selecting Strimzi vs Redpanda Cloud for Kafka (Phase V)

### Review & Evaluation

All development work is subject to process review. Prompts, iterations, and decisions are captured in PHRs for evaluation. This transparency allows for:
- Continuous improvement of development workflow
- Assessment of agent effectiveness across phases
- Identification of complexity justifications
- Validation of spec-driven methodology

## Phase-Specific Standards

### Phase I: Console App Standards

**Deliverables**:
- GitHub repository with constitution, specs, history, src, tests
- README.md with setup instructions
- CLAUDE.md with Claude Code instructions
- Working console application with all 5 Basic Level features

**Success Criteria**:
- Add tasks with title and description
- List all tasks with status indicators
- Update task details by ID
- Delete tasks by ID
- Mark tasks as complete/incomplete

### Phase II: Full-Stack Web Standards

**API Endpoints** (RESTful):
- GET /api/{user_id}/tasks - List all tasks
- POST /api/{user_id}/tasks - Create a new task
- GET /api/{user_id}/tasks/{id} - Get task details
- PUT /api/{user_id}/tasks/{id} - Update a task
- DELETE /api/{user_id}/tasks/{id} - Delete a task
- PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion

**Authentication Flow**:
1. User logs in on Frontend → Better Auth creates session and issues JWT token
2. Frontend makes API call → Includes JWT token in Authorization: Bearer <token> header
3. Backend receives request → Extracts token, verifies signature using shared secret
4. Backend identifies user → Decodes token to get user ID, matches with URL user_id
5. Backend filters data → Returns only tasks belonging to that user

**Security Requirements**:
- All endpoints require valid JWT token
- Requests without token receive 401 Unauthorized
- Each user only sees/modifies their own tasks
- Task ownership enforced on every operation
- Shared secret (BETTER_AUTH_SECRET) used by both frontend and backend

### Phase III: AI Chatbot Standards

**Natural Language Commands** (Agent must understand):
- "Add a task to buy groceries" → add_task
- "Show me all my tasks" → list_tasks(status="all")
- "What's pending?" → list_tasks(status="pending")
- "Mark task 3 as complete" → complete_task(task_id=3)
- "Delete the meeting task" → list_tasks first, then delete_task
- "Change task 1 to 'Call mom tonight'" → update_task
- "I need to remember to pay bills" → add_task(title="Pay bills")

**Agent Behavior Requirements**:
- Task Creation: Detect intent to add/create/remember
- Task Listing: Detect intent to see/show/list with appropriate filter
- Task Completion: Detect intent to mark done/complete/finished
- Task Deletion: Detect intent to delete/remove/cancel
- Task Update: Detect intent to change/update/rename
- Confirmation: Always confirm actions with friendly response
- Error Handling: Gracefully handle task not found and other errors

**Deliverables**:
- /frontend - ChatKit-based UI
- /backend - FastAPI + Agents SDK + MCP
- /specs - Specification files for agent and MCP tools
- Database migration scripts
- README with setup instructions

### Phase IV: Kubernetes Deployment Standards

**Containerization Requirements**:
- Dockerfile for frontend (Next.js)
- Dockerfile for backend (FastAPI)
- Multi-stage builds for optimization
- .dockerignore for build efficiency
- Use Gordon for intelligent container operations

**Helm Chart Requirements**:
- Chart.yaml with version and dependencies
- values.yaml with configurable parameters
- Templates for deployments, services, ingress
- Resource limits and requests defined
- Health checks (liveness, readiness probes)

**Minikube Deployment**:
- Start Minikube with sufficient resources
- Enable required addons (ingress, metrics-server)
- Deploy using Helm install
- Verify pod status and logs
- Test application functionality

### Phase V: Cloud-Native Standards

**Event Schema Standards**:

Task Event:
```json
{
  "event_type": "created|updated|completed|deleted",
  "task_id": 123,
  "task_data": { /* full task object */ },
  "user_id": "user123",
  "timestamp": "2025-01-04T12:00:00Z"
}
```

Reminder Event:
```json
{
  "task_id": 123,
  "title": "Task title",
  "due_at": "2025-01-05T09:00:00Z",
  "remind_at": "2025-01-05T08:00:00Z",
  "user_id": "user123"
}
```

**Dapr Component Configuration**:
- pubsub.kafka for event streaming
- state.postgresql for conversation state
- Jobs API for scheduled triggers
- secretstores.kubernetes for credentials

**CI/CD Pipeline Requirements** (GitHub Actions):
- Automated testing on pull requests
- Container image builds
- Helm chart linting and validation
- Deployment to staging environment
- Deployment to production (manual approval)

**Observability Requirements**:
- Structured logging (JSON format)
- Metrics collection (Prometheus-compatible)
- Distributed tracing (OpenTelemetry)
- Alerting for critical failures

## Governance

### Constitution Versioning

The constitution follows semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Backward incompatible changes to principles or fundamental workflow changes (e.g., 1.x.x → 2.0.0)
- **MINOR**: New principle or section added, or materially expanded guidance (e.g., 2.0.x → 2.1.0)
- **PATCH**: Clarifications, wording improvements, non-semantic refinements (e.g., 2.1.0 → 2.1.1)

### Amendment Process

Amendments to the constitution MUST:
1. Update the version number according to semantic versioning rules
2. Document changes in the Sync Impact Report (HTML comment at top of file)
3. Update dependent templates and command files to maintain consistency
4. Be reviewed for compliance with existing principles before approval
5. Include rationale for version bump (MAJOR vs MINOR vs PATCH)

### Compliance Review

All development work MUST comply with constitution principles:
- Spec-Driven Development workflow MUST be followed in all phases
- Agentic Implementation via Claude Code MUST be used (no manual coding)
- Clean Code standards MUST be maintained across all languages
- Tests MUST pass before phase completion
- PHRs MUST be created for all interactions with phase context
- Phase progression MUST follow validation checkpoints

### Complexity Justification

Any deviation from simple architecture or introduction of new complexity MUST be documented in the Complexity Tracking section of implementation plans. The justification MUST:
1. Explain why the simpler alternative is insufficient
2. Reference specific requirements driving the complexity
3. Demonstrate that the complexity is necessary for the current phase
4. Identify the simpler approach that was rejected and why

**Examples**:
- Phase II: Database persistence justified by multi-user requirements (in-memory insufficient)
- Phase III: MCP server justified by AI agent tool integration requirements
- Phase V: Kafka justified by event-driven requirements (recurring tasks, reminders, real-time sync)

**Prohibited**: Adding complexity for "future-proofing", "industry best practices", or "scalability" without clear current requirements.

### Phase Transition Criteria

Transition to the next phase is only permitted when:
1. All P1 (Priority 1) user stories are complete and tested
2. All acceptance criteria for current phase are met
3. Phase-specific deliverables are complete and validated
4. Architecture Decision Records (ADRs) are documented for significant decisions
5. Prompt History Records (PHRs) are complete and organized
6. User approval is obtained for phase transition

**Version**: 2.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2026-01-04
