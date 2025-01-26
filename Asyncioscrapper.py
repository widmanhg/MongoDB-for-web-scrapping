import asyncio
import subprocess

async def run_script(script_name):
    """
    Ejecuta un script de Python como un subproceso.
    """
    try:
        process = await asyncio.create_subprocess_exec(
            "python", script_name,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if stdout:
            print(f"Salida de {script_name}:\n{stdout.decode()}")
        if stderr:
            print(f"Errores en {script_name}:\n{stderr.decode()}")
    except Exception as e:
        print(f"Error al ejecutar {script_name}: {e}")

async def main():
    """
    Ejecuta ambos scripts con un retraso de 5 segundos entre ellos.
    """
    # Ejecuta `urls.py` primero
    print("Ejecutando urls.py...")
    urls_task = asyncio.create_task(run_script("urls.PY"))

    # Espera a que `urls.py` inicie y ejecuta `info.py` después de 5 segundos
    await asyncio.sleep(5)
    print("Ejecutando info.py después de 5 segundos...")
    info_task = asyncio.create_task(run_script("info.py"))

    # Espera a que ambos scripts finalicen
    await asyncio.gather(urls_task, info_task)

if __name__ == "__main__":
    asyncio.run(main())
