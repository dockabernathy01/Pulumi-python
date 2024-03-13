import asyncio
 
async def set_config(config_key, config_value):
    cmd = f'pulumi config set {config_key} {config_value}'
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        print(f'Error: {stderr.decode()}')

async def pulumi_up():
    cmd = 'pulumi up --non-interactive --yes'
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        print(f'Error: {stderr.decode()}')

async def main():
    # Set repository name
    await set_config('_name', 'desired-repo-name')
    
    # Set repository visibility
    await set_config('repo_visibility', 'private')
    
    # Perform pulumi up
    await pulumi_up()

# Create a new event loop
asyncio.set_event_loop(asyncio.new_event_loop())

# Run the tasks
asyncio.run(main())