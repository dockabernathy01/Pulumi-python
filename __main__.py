"""A Python Pulumi program"""

import pulumi
import pulumi_github as github
import pulumi_cloudflare as cloudflare

# Input domain name for the new repository and site
domain_name = "example.com"
github_provider = github.Provider('github-provider')
# Create a new private GitHub repository from the existing template
# new_repo = github.Repository("new-repo",
#     name=domain_name,
#     description="Demo Repository for GitHub",
#     visibility="private",
#     opts=pulumi.ResourceOptions(provider=github_provider),
#     template=github.RepositoryTemplateArgs(
#         owner="MOONSTAR0515", # Replace with your GitHub organization name
#         repository="landing_template" # Replace with your repository template name
#     )
# )

new_repo = github.Repository("new-repo",
    name=domain_name,  # Name for your new repository
    description="A new repository from a landing template",
    visibility="private",    # or "private" based on your needs
    # opts=pulumi.ResourceOptions(provider=github_provider),
    template=github.RepositoryTemplateArgs(
        owner="MOONSTAR0515",
        repository="landing_template",
        include_all_branches=False
    ))

# Connect the repository to Cloudflare Pages
pages_project = cloudflare.PagesProject("pages-project",
    name=domain_name,
    account_id="cloudflare-account-id", # Replace with your Cloudflare account ID
    production_branch="main", # Default production branch
    build_config=cloudflare.PagesProjectBuildConfigArgs(
        # Default build settings, customize as needed
        build_command="npm run build",
        destination_dir="build",
    ),
    source=cloudflare.PagesProjectSourceArgs(
        # GitHub details, might need additional configurations
        type="github",
        config=cloudflare.PagesProjectSourceConfigArgs(
            owner="github-organization", # Use the same GitHub organization name
            repo_name=new_repo.name,
            production_branch="main", # Match with production_branch above
        )
    )
)

# # Add DNS records to Cloudflare for the domain
# # Replace with the actual zone ID for the domain in Cloudflare
# zone_id = "cloudflare-zone-id"

# # Add an 'A' record for the root domain
# root_record = cloudflare.Record("root-record",
#     zone_id=zone_id,
#     name=domain_name,
#     type="A",
#     value="192.0.2.1", # Use the actual IP address or use Pages IP
#     proxied=True
# )

# # Add a 'CNAME' record for a development environment (e.g., 'dev')
# dev_record = cloudflare.Record("dev-record",
#     zone_id=zone_id,
#     name=f"dev.{domain_name}",
#     type="CNAME",
#     value=pages_project.name.apply(lambda name: f"{name}.pages.dev"), # Points to Cloudflare Pages dev environment
#     proxied=True
# )

# # Export the new repository's HTTPS clone URL and the DNS record names
pulumi.export("github_repository_url", new_repo.html_url)
# pulumi.export("root_record_name", root_record.name)
# pulumi.export("dev_record_name", dev_record.name)