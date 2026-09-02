from library_path.application.builder.build_path_use_case import BuildPathUseCase
from library_path.application.builder.command import BuildPathCommand
from library_path.domain.entities import Project, Sequence, Shot, Task, Version, WorkType
from library_path.infrastructure.path_templates import InMemoryPathTemplateRepository
from library_path.infrastructure.template_renderer import FormatStringPathRenderer


build_path = BuildPathUseCase(
    template_repository=InMemoryPathTemplateRepository.with_default_vfx_templates(),
    renderer=FormatStringPathRenderer(),
)

command = BuildPathCommand(
    project=Project(code="dragon"),
    entity=Shot(
        sequence=Sequence(code="sq010"),
        code="sh020",
    ),
    task=Task(name="lighting"),
    version=Version(number=12),
    work_type=WorkType.PUBLISH,
    extension="abc",
)

result = build_path.execute(command)

print(result.as_string)
