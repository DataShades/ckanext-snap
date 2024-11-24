[![Tests](https://github.com/DataShades/ckanext-snap/workflows/tests.yml/badge.svg)](https://github.com//ckanext-snap/actions/workflows/test.yml)

# ckanext-snap

Save and restore state of packages, resources, groups, etc.

Read the [documentation](https://datashades.github.io/ckanext-snap/) for a full user guide.

## Requirements

Compatibility with core CKAN versions:

| CKAN version | Compatible? |
|--------------|-------------|
| 2.9          | no          |
| 2.10         | yes         |
| 2.11         | yes         |
| master       | yes         |

## Quickstart

Install the extension
```sh
pip install ckanext-snap
```

Add `snap` to the list of enabled CKAN plugins.

Create snapshot using `snap_snapshot_create` API action:
```sh
ckanapi action snap_snapshot_create target_id=<PACKAGE_ID> target_type=package
```

## Development

Install the
```sh
git clone https://github.com/DataShades/ckanext-snap.git
cd ckanext-snap
pip install -e '.[dev]'
```

Run tests:
```sh
pytest
```


## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
