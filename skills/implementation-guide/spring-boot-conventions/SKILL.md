---
name: spring-boot-conventions
description: >
  House project conventions for Java 27 / Spring Boot 4.1.1 REST API projects on Gradle — layered
  architecture, coding conventions, database/migration naming, REST controller shape, exception
  handling, testing, and git conventions. Loaded unconditionally for every Java context by
  implementation-guide, never resolved per-topic.
---
# Java and Spring Boot Project Instructions

Java 27 + Spring Boot 4.1.1 REST API. Gradle build system. PostgreSQL database with Spring Data JPA.

## Workflow

- **Implement** — constructor injection, layered architecture (see `## Architecture` below)
- **Secure** — apply Spring Security/OAuth2/method security per `skills/security/spring-security-jwt`
  and `skills/security/oauth2-resource-server` where the context calls for it
- **Test** — write unit + integration tests (see `## Testing` below), run `./gradlew check`, confirm all pass
- **Deploy** — expose health checks via Spring Boot Actuator; validate `/actuator/health` returns `UP`

## Commands

- `./gradlew bootRun` — start the server
- `./gradlew test` — run all tests
- `./gradlew test --tests "packages.className"` — run a single test class by mentioning packages and specific class name
- `./gradlew test --tests "*.className.methodName"` — run a single test method of a specific class
- `./gradlew spotlessCheck` — check code formatting
- `./gradlew spotlessApply` — auto-format code
- `./gradlew check` — run all checks (tests + spotless + checkstyle)
- `docker compose up -d` — start all containers

Run `./gradlew check` before committing.

## Architecture

Standard layered Spring Boot architecture:

- `src/main/java/com/` `—`Where all Java source files exist
  - `controller/` — REST controllers, one per resource
  - `service/` — business logic, interfaces + implementations
  - `repository/` — Spring Data JPA repositories
  - `model/` — JPA entity classes
  - `dto/` — request/response DTOs (records)
  - `mapper/` — MapStruct mappers for entity-DTO conversion
  - `config/` — Spring configuration classes
  - `exception/` — custom exceptions and global exception handler
  - `security/` — Spring Security configuration and filters
- `src/main/resources/`
  - `application.yml` — main config
  - `application-staging.yml` — staging overrides
  - `application-local.yml` — local dev overrides
  - `db/migration/` — Flyway migration scripts
- `src/test/java/` — mirrors main structure

## Coding Conventions

- Java 27 (this catalog's only supported version and language-feature usage — see `../java-language-conventions/SKILL.md`): use records for DTOs, pattern matching, sealed interfaces, and newer language surface where it earns its keep
- Constructor injection only — no field injection with `@Autowired`
- Use `final` on all fields, parameters, and local variables where possible
- DTOs are Java records, not classes:

```java
public record CreateCustomerRequest(
    @NotBlank String name,
    @Email String email,
    @NotNull CustomerType type
) {}
```

- Service interfaces with single implementation: `CustomerService` interface + `CustomerServiceImpl`
- All public methods in services have Javadoc
- Use `Optional<T>` return types for single-entity lookups — never return null
- Use `lombok` only for `@Slf4j` — do not use `@Data`, `@Getter`, `@Setter` on new code (use records)

## Database

- Flyway for migrations — files in `src/main/resources/db/migration/`
- Naming: `V001__create_customers_table.sql`, `V002__add_email_index.sql`
- JPA entities use `@Entity` with explicit `@Table(name = "...")` and `@Column(name = "...")`
- Always specify column lengths and constraints in the entity
- Use `@Version` for optimistic locking on frequently updated entities
- Repositories extend `JpaRepository<T, ID>` — add custom query methods with `@Query` or derived queries

```java
@Entity
@Table(name = "customers")
public class Customer {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", nullable = false, length = 255)
    private String name;

    @Column(name = "email", nullable = false, unique = true)
    private String email;

    @Version
    private Long version;
}
```

## REST Controllers

```java
@RestController
@RequestMapping("/api/v1/customers")
@RequiredArgsConstructor
public class CustomerController {
    private final CustomerService customerService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public CustomerResponse create(@Valid @RequestBody CreateCustomerRequest request) {
        return customerService.create(request);
    }

    @GetMapping("/{id}")
    public CustomerResponse getById(@PathVariable Long id) {
        return customerService.getById(id);
    }
}
```

- Use `@Valid` on all request body parameters
- Return DTOs, never entities
- Use `@ResponseStatus` for non-200 success codes
- Paginated endpoints return `Page<T>` with Spring's `Pageable` parameter

## Exception Handling

Global exception handler in `exception/GlobalExceptionHandler.java`:

- `@RestControllerAdvice` with `@ExceptionHandler` methods
- Custom exceptions: `ResourceNotFoundException`, `BusinessValidationException`, `ConflictException`
- Return structured error responses: `{ "error": "...", "code": "...", "timestamp": "..." }`
- Never expose stack traces or internal details in error responses

## Testing

- Unit tests: JUnit 5 + Mockito for service layer
- Integration tests: `@SpringBootTest` with Testcontainers for database
- Controller tests: `@WebMvcTest` with `MockMvc`
- Use `@Sql` annotation to load test data from SQL files
- Test naming: `should_[expected]_when_[condition]` — e.g., `should_throw_not_found_when_customer_missing`
- Test data builders in `src/test/java/.../fixture/`

## Git

- Conventional commits: feat:, fix:, chore:, refactor:
- One feature per PR, squash merge to main
- Run `./gradlew check` before pushing

## Do NOT

- Do not use field injection (`@Autowired` on fields)
- Do not return JPA entities from controllers — always map to DTOs
- Do not use `@Data` or `@Getter`/`@Setter` on new code — use records or write accessors
- Do not catch `Exception` or `RuntimeException` in service code — let the global handler deal with it
- Do not use `System.out.println` — use SLF4J logging (`@Slf4j`)
- Do not write business logic in controllers — delegate to the service layer
- Do not store secrets in `application.yml`/`application.properties` — use environment variables
- Do not mix blocking and reactive code in the same service
- Do not hardcode URLs, credentials, or other environment-specific values
