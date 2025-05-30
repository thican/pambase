#!/usr/bin/env python3

import argparse
from jinja2 import Template, Environment, FileSystemLoader
import pathlib


def main():
    parser = argparse.ArgumentParser(description="basic Gentoo PAM configuration files")
    parser.add_argument(
        "--gnome-keyring",
        action="store_true",
        help="enable pam_gnome_keyring.so module",
    )
    parser.add_argument("--caps", action="store_true", help="enable pam_cap.so module")
    parser.add_argument(
        "--passwdqc", action="store_true", help="enable pam_passwdqc.so module"
    )
    parser.add_argument(
        "--pwhistory", action="store_true", help="enable pam_pwhistory.so module"
    )
    parser.add_argument(
        "--pwquality", action="store_true", help="enable pam_pwquality.so module"
    )
    parser.add_argument(
        "--openrc", action="store_true", help="enable pam_openrc.so module"
    )
    parser.add_argument(
        "--elogind", action="store_true", help="enable pam_elogind.so module"
    )
    parser.add_argument(
        "--systemd", action="store_true", help="enable pam_systemd.so module"
    )
    parser.add_argument(
        "--homed", action="store_true", help="enable pam_systemd_home.so module"
    )
    parser.add_argument(
        "--selinux", action="store_true", help="enable pam_selinux.so module"
    )
    parser.add_argument(
        "--mktemp", action="store_true", help="enable pam_mktemp.so module"
    )
    parser.add_argument(
        "--pam-ssh", action="store_true", help="enable pam_ssh.so module"
    )
    parser.add_argument(
        "--securetty", action="store_true", help="enable pam_securetty.so module"
    )
    parser.add_argument(
        "--shells", action="store_true", help="enable pam_shells.so module"
    )
    parser.add_argument("--sssd", action="store_true", help="enable sssd.so module")
    parser.add_argument(
        "--encrypt",
        choices=["md5", "sha256", "sha512", "blowfish", "gost_yescrypt", "yescrypt"],
        default="md5",
        help="select encryption to use for passwords stored by pam_unix.so module",
    )
    parser.add_argument("--krb5", action="store_true", help="enable pam_krb5.so module")
    parser.add_argument(
        "--minimal", action="store_true", help="install minimalistic PAM stack"
    )
    parser.add_argument(
        "--debug",
        action="store_const",
        const="debug",
        default="",
        help="enable debug for selected modules",
    )
    parser.add_argument(
        "--nullok",
        action="store_const",
        const="nullok",
        default="",
        help="enable nullok option for pam_unix.so module",
    )

    parsed_args = parser.parse_args()
    processed = process_args(parsed_args)

    parse_templates(processed)


def process_args(args):
    # make sure that output directory exists
    pathlib.Path("stack").mkdir(parents=True, exist_ok=True)

    output = vars(args)

    return output


def parse_templates(processed_args):
    load = FileSystemLoader("")
    env = Environment(
        loader=load, trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True
    )

    templates = [
        "login",
        "other",
        "passwd",
        "system-local-login",
        "system-remote-login",
        "su",
        "system-auth",
        "system-login",
        "system-services",
    ]

    for template_name in templates:
        template = env.get_template("templates/{0}.tpl".format(template_name))

        with open("stack/{0}".format(template_name), "w+") as output:
            rendered_template = template.render(processed_args)

            # Strip all intermediate lines to not worry about appeasing Jinja
            lines = rendered_template.split("\n")
            lines = [line.strip() for line in lines if line]
            rendered_template = "\n".join(lines)

            if rendered_template:
                output.write(rendered_template + "\n")


if __name__ == "__main__":
    main()
