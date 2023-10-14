# Spring2023 - Security Analysis Of Bluetooth Low Energy Over The Air Firmware Updates

- [Spring2023 - Security Analysis Of Bluetooth Low Energy Over The Air Firmware Updates](#spring2023-security-analysis-of-bluetooth-low-energy-over-the-air-firmware-updates)
  - [About](#about)
  - [Some notes and important files and folders](#some-notes-and-important-files-and-folders)
  - [Folder structures](#folder-structures)
  - [References](#references)

## About

This is a semester project in Master program in Eurecom  under instruction of professor [Aurelien Francillon] and [Romain Cayre].

Goals:

- Reverse engineer the OTA firmware update process on nRF51 and nRF52 chips from Nordic Semiconductor, document its internals and identify potential vulnerabilities.
- Evaluate the attack surface exposed by this critical service and estimate if an attacker can compromise the target device by injecting a malicious firmware update.

See [this project description file][1-references] for the introduction of the project.

## Some notes and important files and folders

## Folder structures

See [this file](notes/folder_tree.md) for the folder structures of this repository.

## References

- [Getting Started with Bluetooth Low Energy (O'reilly), by Kevin Townsend, Carles Cufi, Akiba and Robert Davidson](notes/References/Getting%20Started%20with%20Bluetooth%20Low%20Energy.pdf)
- [Inside Bluetooth Low Energy (Artech House), by Naresh Gupta](notes/References/Inside%20Bluetooth%20Low%20Energy,%20Second%20Edition.pdf)
- [Bluetooth Specification Core v4.2](notes/References/Core_v4.2.pdf)

 <a href="#top">Back to top</a>

 [1-references]: /notes/References/2023spring-05_analysis_of_bluetooth_low_energy_ota_firmware_updates_francillon.pdf

[Aurelien Francillon]: https://www.eurecom.fr/fr/people/francillon-aurelien

[Romain Cayre]: https://www.eurecom.fr/fr/people/cayre-romain
