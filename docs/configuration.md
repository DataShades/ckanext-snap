## `ckanext.snap.tracked_actions`

Actions that automatically create a snapshot for their result.

By default, target type is set to the action name before the last
underscore. I.e, `package_create` produces `package` type, `x_y_z` produces
`x_y` type. To override it, append type to the action name using colon as
separator. `organization_create:group` produces `group` type for snapshot.

ID of the target is taken from `id` property inside the action result. To
modify the name of the property, append new name to the action after a second
column. `user_create::name` produces snapshot for `user` using its `name` as a
target id.

Custom target type and ID can be combined: `user_create:person:email` will
create snapshot with `person` as type and value of `email` as an ID.

## `ckanext.snap.restorable_types`

Types of snapshot target than can restore their previous state.

By default, target type is combined with `_update` suffix and the result is
used as a name of the action that restores previous state. To use a different
action, append it to the type using a colon as a separator. I.e,
`dataset:package_update` to use `package_update` action whenever the state of
`dataset` target is restored.
