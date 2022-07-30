#! /usr/bin/env python3
"""Version increment utility."""
import sys
import semver


def main():
    """Increment version passed as first script parameter."""
    try:
        original_version = sys.argv[1]
        # transform from pep 440 to semver
        version = original_version.replace(".dev", "-rc.")
    except IndexError:
        print("Usage: is_release.py VERSION", file=sys.stderr)
        sys.exit(1)
    vinfo = semver.VersionInfo.parse(version)
    if vinfo.prerelease is None and vinfo.build is None:
        print("{} is a release version".format(original_version))
        sys.exit(0)
    else:
        print("{} is not a release version".format(original_version))
        sys.exit(1)

if __name__ == '__main__':
    main()
