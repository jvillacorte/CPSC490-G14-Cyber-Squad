from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class SimulatedFile(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    path: str
    contents: str

    @field_validator("path")
    @classmethod
    def valid_virtual_path(cls, path: str) -> str:
        parts = path.split("/")
        if (
            not path.startswith("/")
            or "\\" in path
            or "\x00" in path
            or any(part in ("", ".", "..") for part in parts[1:])
        ):
            raise ValueError("A file path must be an absolute, normalized virtual path")
        return path


class Scenario(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    files: tuple[SimulatedFile, ...] = Field(min_length=1, strict=False)

    @model_validator(mode="after")
    def unique_paths(self) -> "Scenario":
        paths = [file.path for file in self.files]
        if len(paths) != len(set(paths)):
            raise ValueError("Simulated file paths must be unique")
        return self
