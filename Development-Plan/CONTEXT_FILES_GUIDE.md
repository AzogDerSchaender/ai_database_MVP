# Context Files Guide for Multi-Agent Database AI MVP

## Overview

This guide explains how to use the 38 context files created for the Multi-Agent Database AI MVP Development Plan. These files are designed to minimize LLM mistakes and hallucinations by providing comprehensive, structured context for each prompt.

## What Are Context Files?

Context files are detailed guides that accompany each development prompt. They provide:
- Technical specifications and requirements
- Security considerations and best practices
- Testing strategies and coverage requirements
- Integration points with existing code
- Performance targets and benchmarks
- Implementation checklists
- Common patterns and anti-patterns

## Structure of Each Context File

Each context file follows this structure:

1. **LLM Recommendation**: Suggests the best LLM for the task
2. **Prompt Overview**: Phase, position, and dependencies
3. **Original Prompt**: The exact prompt from the Development Plan
4. **Project Context**: Current state and structure
5. **Implementation Requirements**: What needs to be built
6. **Technical Specifications**: Architecture and design patterns
7. **Security Considerations**: Critical security requirements
8. **Testing Strategy**: Comprehensive testing approach
9. **Code Quality Standards**: Style and documentation requirements
10. **Implementation Checklist**: Step-by-step validation
11. **Notes for LLM**: Specific guidance to prevent errors

## How to Use Context Files

### For Developers/Users:

1. **Before Starting a Prompt**:
   - Open the corresponding context file
   - Review all sections, especially dependencies
   - Ensure previous prompts are completed
   - Set up your development environment

2. **During Implementation**:
   - Keep the context file open for reference
   - Follow the implementation checklist
   - Use the provided code patterns
   - Adhere to security guidelines

3. **After Implementation**:
   - Validate against success criteria
   - Run all specified tests
   - Check performance requirements
   - Update documentation

### For LLMs:

When providing a prompt to an LLM:
1. Include the entire context file with your prompt
2. Reference specific sections when asking questions
3. Use the checklist to validate completeness
4. Pay attention to the "Notes for LLM" section

## Security-First Approach

Every context file emphasizes security:
- **Input Validation**: Always validate and sanitize inputs
- **SQL Injection Prevention**: Use parameterized queries
- **Authentication**: Implement proper access controls
- **Error Handling**: Never expose internal errors
- **Audit Logging**: Track all sensitive operations

## Testing Requirements

Each prompt includes comprehensive testing:
- **Unit Tests**: >90% code coverage required
- **Integration Tests**: Component interaction testing
- **Security Tests**: Vulnerability scanning
- **Performance Tests**: Meeting specified benchmarks
- **E2E Tests**: Full workflow validation

## Performance Standards

All implementations must meet:
- Response times specified in context files
- Resource usage limits
- Scalability requirements
- Concurrent operation support

## Best Practices

1. **Follow the Order**: Complete prompts in sequence
2. **Don't Skip Steps**: Each builds on the previous
3. **Test Continuously**: Write tests as you code
4. **Document Everything**: Future developers need context
5. **Review Security**: Every component has security implications

## Common Pitfalls to Avoid

1. **Skipping Dependencies**: Each prompt depends on previous work
2. **Ignoring Security**: Security is not optional
3. **Incomplete Testing**: All test types are required
4. **Poor Documentation**: Code without docs is incomplete
5. **Performance Afterthoughts**: Design for performance from start

## File Naming Convention

Context files follow this pattern:
```
prompt_<phase>_<number>_<title_with_underscores>.md
```

Example: `prompt_1_4_sandbox_environment_and_safety.md`

## Integration with Cursor

These context files are optimized for Cursor AI:
- Use multi-file editing for related components
- Leverage codebase-wide search for consistency
- Apply AI suggestions with security in mind
- Maintain pattern consistency across files

## Quality Assurance

Each context file includes:
- Implementation checklist
- Success criteria
- Performance requirements
- Security validations
- Testing requirements

## Maintenance

As the project evolves:
- Update context files with lessons learned
- Add new patterns discovered during development
- Document any deviations from original plans
- Keep security guidelines current

## Support

If you encounter issues:
1. Check the context file's troubleshooting section
2. Review dependencies and prerequisites
3. Ensure all tests pass
4. Validate against the checklist

## Conclusion

These context files are your roadmap to building a production-ready Multi-Agent Database AI system. By following them carefully, you'll create a secure, scalable, and maintainable solution while minimizing errors and development time.

Remember: **Security First, Test Everything, Document Thoroughly**
