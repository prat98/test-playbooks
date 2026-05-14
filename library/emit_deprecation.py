#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r'''
---
module: emit_deprecation
short_description: Emit a structured Ansible deprecation warning
description:
  - Calls AnsibleModule.deprecate() to emit a structured deprecation warning.
  - Each unique message produces a separate deprecated event captured by AWX/AAP
    and visible in the Deprecations Dashboard.
  - Use different messages per invocation to avoid Ansible's deduplication.
options:
  message:
    description: The deprecation message text (must be unique per warning).
    required: true
    type: str
  version:
    description: The Ansible version when the feature will be removed.
    required: false
    type: str
    default: '2.19'
'''

EXAMPLES = r'''
- name: Emit a deprecation warning
  emit_deprecation:
    message: "Feature foo is deprecated, use bar instead"
    version: "2.19"

- name: Emit 200 unique deprecation warnings
  emit_deprecation:
    message: "Deprecated feature {{ item.name }} ({{ item.id }})"
    version: "2.19"
  loop: "{{ deprecated_features }}"
'''

RETURN = r'''
message:
  description: The deprecation message that was emitted.
  returned: always
  type: str
'''

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            message=dict(type='str', required=True),
            version=dict(type='str', default='2.19'),
        ),
        supports_check_mode=True,
    )

    msg = module.params['message']
    version = module.params['version']

    module.deprecate(msg, version=version)

    module.exit_json(changed=False, message=msg)


if __name__ == '__main__':
    main()
