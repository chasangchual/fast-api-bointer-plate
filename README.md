
## Dependency Management

### Renew the uv dependencies with the latest version 

To update dependencies to their latest versions using uv, you can use the uv lock or uv sync commands with specific upgrade flags. Note that uv differentiates between updating the versions stored in your lockfile and updating the version constraints defined in your pyproject.toml file. 

```bash
uv lock --upgrade
```

These commands update the locked versions of your packages to the latest versions that still satisfy the constraints in your pyproject.toml.

Update specific packages: Use uv lock --upgrade-package <package_name> to update only a specific package (and its dependencies if necessary) while keeping the rest of the lockfile intact.


```bash
uv lock --upgrade-package <package>
```

Manual Update Workaround: To explicitly change the version in pyproject.toml to the latest version, you can manually edit the file or use uv add <package_name> again, which will re-resolve the latest version and update the file accordingly. Then run `uv sync` to sync the runtime environments.


### Set up the environment 

`uv sync`  is the primary command used to ensure your local development environment exactly matches your project's defined requirements. It acts as an "all-in-one" synchronization tool that automates several setup steps in a single fast operation. 


```bash
uv sync
```

**Core Functions**

When you run uv sync, the tool performs the following actions in order:
* Python Discovery: It finds or downloads the appropriate Python version defined in your pyproject.toml.
* Environment Management: It creates a virtual environment (typically in .venv/) if one doesn't exist.
* Lockfile Resolution: It resolves all project dependencies and updates the uv.lock file to ensure consistency.
* Exact Installation: It installs the exact versions from the lockfile into your environment.
* Clean Up: By default, it performs an exact sync, meaning it uninstalls any "extraneous" packages in the environment that are not listed in the lockfile. 