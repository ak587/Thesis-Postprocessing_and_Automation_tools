from pathlib import Path
import subprocess

ROOT = Path.cwd()
FLUENT_EXE = Path(r"C:\Program Files\ANSYS Inc\v232\fluent\ntbin\win64\fluent.exe")

NAMES = [
    "T300K_M0.4_TI5_2bar",
    "T350K_M0.4_TI5_2bar",
    "T400K_M0.4_TI5_2bar",
    "T600K_M0.4_TI5_2bar",
    "T300K_M0.45_TI5_2bar",
    "T600K_M0.45_TI5_2bar",
    "TI0.1_M0.4_T300K_2bar",
    "TI1_M0.4_T300K_2bar",
    "TI5_M0.4_T300K_2bar",
    "TI10_M0.4_T300K_2bar",
    "M0.076_TI5_T300K_2bar",
    "M0.26_TI5_T300K_2bar",
    "M0.4_TI5_T300K_2bar",
    "M0.45_TI5_T300K_2bar",
    "M0.47_TI5_T300K_2bar",
    "M0.48_TI5_T300K_2bar",
    "1bar_M0.4_TI10_T300K",
    "2bar_M0.4_TI10_T300K",
    "5bar_M0.4_TI10_T300K",
    "10bar_M0.4_TI10_T300K",
    "20bar_M0.4_TI10_T300K",
]

CASEFILES = [
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Temperature-analysis\T300K_M0.4_TI5_2bar.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Temperature-analysis\T350K_M0.4_TI5_2bar.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Temperature-analysis\T400K_M0.4_TI5_2bar.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Temperature-analysis\T600K_M0.4_TI5_2bar.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Mach-analysis\M0.45_TI5_T300K_2bar.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Temperature-analysis\T600K_M0.45_TI5_2bar.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\TI-analysis\TI0.1_M0.4_T300K_2bar.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\TI-analysis\TI1_M0.4_T300K_2bar.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\TI-analysis\TI5_M0.4_T300K_2bar.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\TI-analysis\TI10_M0.4_T300K_2bar.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Mach-analysis\M0.076_TI5_T300K_2bar.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Mach-analysis\M0.26_TI5_T300K_2bar.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Mach-analysis\M0.4_TI5_T300K_2bar.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Mach-analysis\M0.45_TI5_T300K_2bar.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Mach-analysis\M0.47_TI5_T300K_2bar.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Mach-analysis\M0.48_TI5_T300K_2bar.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Re-analysis\1bar_M0.4_TI10_T300K.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Re-analysis\2bar_M0.4_TI10_T300K.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Re-analysis\5bar_M0.4_TI10_T300K.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Re-analysis\10bar_M0.4_TI10_T300K.cas.h5",
    r"C:\Users\ak587\Desktop\Work\Post-processing\HPC_downloader\Re-analysis\20bar_M0.4_TI10_T300K.cas.h5"
]

CUSTOM_SURFACE = [0, 2.5, 5]
MASTER_JOURNAL = ROOT / "export_all.jou"

with open(MASTER_JOURNAL, "w") as f:
    f.write(f'file set-batch-opt y y y n\n')
    for name, casefile in zip(NAMES, CASEFILES):

        casefile_location = str(casefile)
        output_base = str((ROOT / name))

        f.write(f'\n/file/read-case-data "{casefile_location}" OK\n')

        for i in range(7):
            if i < 2:
                f.write(f'surface/plane-surface upstream-{i+1}d xy-plane {-50*(i+1)}\n')
            else:
                f.write(f'surface/plane-surface downstream-{i-1}d xy-plane {50*(i-1)+5}\n')

        for i in range(7):
            if i < 2:
                f.write(f'file/export/cgns "{output_base}_upstream-{i+1}d.cgns"'
                        f'surface-select upstream-{i+1}d () no yes '
                        f'x-velocity y-velocity z-velocity mach-number total-pressure ()\n'
                )
            else:
                f.write(f'file/export/cgns "{output_base}_downstream-{i-1}d.cgns"'
                        f'surface-select downstream-{i-1}d () no yes '
                        f'x-velocity y-velocity z-velocity mach-number total-pressure ()\n'
                )

        for i in CUSTOM_SURFACE:
            f.write(f'surface/plane-surface screen_{i}mm xy-plane {i}\n')
            f.write(
                f'/file/export/cgns "{output_base}_screen_{i}mm.cgns" '
                f'surface-select screen_{i}mm () no yes '
                f'x-velocity y-velocity z-velocity mach-number total-pressure ()\n'
            )

    f.write("\n/exit yes\n")

print("Journal file created.")

cmd = [
    str(FLUENT_EXE),
    "3ddp",
    "-g",
    "-t1",
    "-i",
    str(MASTER_JOURNAL.resolve())
]

print("Launching Fluent...")
subprocess.run(cmd)
print("Done.")
