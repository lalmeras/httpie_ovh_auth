#! /usr/bin/env python3
"""Version increment utility."""
import sys
import semver


def main():
    """Increment version passed as first script parameter."""
    try:
        part = sys.argv[1]
        version = sys.argv[2]
        # transform from pep 440 to semver
        version = version.replace(".dev", "-rc.")
    except IndexError:
        print("Usage: version.py (major|minor|path|dev) VERSION", file=sys.stderr)
        sys.exit(1)
    allowed_parts = ("major", "minor", "patch", "dev")
    if not part in allowed_parts:
        print(f"{part} not in {allowed_parts}")
        sys.exit(1)
    new_version = str(semver.VersionInfo.parse(version).next_version(part="prerelease" if part == "dev" else part))
    new_version = new_version.replace("-rc.", ".dev")
    print(new_version)
    sys.exit(0)


if __name__ == '__main__':
    main()
