import shlex, subprocess, tempfile, sys

from myPyApps import myapp, mylogging, myargparse

LOGGER = mylogging.getLogger(__name__)

class PyBatch(myapp.MyApp):

    def main(self):
        if self.get_option('list'):
            if self.CONFIG.sections():
                print("Configuration sections are :")
                print("\n".join(self.CONFIG.sections()))
            else:
                print("No configuration section are defined.")
            return None

        section = self.get_option("section")
        # validate section
        if section not in self.CONFIG.sections():
            raise ValueError("Section %r does not exist in config" % section)
        status = self._process_section(section)
        if not self.CONFIG.getboolean(section, 'fail_on_error'):
            return None
        else:
            return status

    def _process_section(self, section):
        """ execute section command """
        _command = self.CONFIG.get(section, 'command')
        LOGGER.info("Run command %r (section %r)" % (_command, section))
        _args = shlex.split(_command)

        _email_on_success = self.CONFIG.getboolean(section, 'email_on_success')
        _email_on_error = self.CONFIG.getboolean(section, 'email_on_error')
        _console_stdout = self.CONFIG.getboolean(section, 'console_stdout')
        _console_stderr = self.CONFIG.getboolean(section, 'console_stderr')
        _fail_on_error = self.CONFIG.getboolean(section, 'fail_on_error')
        _shell = self.CONFIG.getboolean(section, 'shell')
        LOGGER.debug("config for section %r is "
                     "_email_on_success = %r, "
                     "_email_on_error = %r, "
                     "_console_stdout = %r, "
                     "_console_stderr = %r, "
                     "_fail_on_error = %r, "
                     "_shell = %r" %
                     (section, _email_on_success, _email_on_error, _console_stdout, _console_stderr, _fail_on_error, _shell))

        if self.get_option('dry_run'):
            LOGGER.info("[dry-run] should have run command %r for section %r" % (_args, section))
            return

        with tempfile.NamedTemporaryFile(mode='r+t', prefix=section+'_', suffix='.txt') as file:
            LOGGER.debug("create temporary file %r" % file.name)
            proc = subprocess.Popen(_args, shell=_shell, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            with proc.stdout, proc.stderr:
                for line in iter(proc.stdout.readline, b''):
                    if _console_stdout:
                        sys.stdout.write(line)
                    file.write(line)
                for line in iter(proc.stderr.readline, b''):
                    if _console_stderr:
                        sys.stderr.write(line)
                    file.write(line)
            proc.wait()
            status = proc.returncode
            file.seek(0)
            LOGGER.debug("done with command for section %r with status %r" % (section, status))
            if not self.get_option(myargparse.QUIET):
                if status and _email_on_error:
                    LOGGER.debug("sending email for batch failure")
                    LOGGER.send_email(file.read(), "[pybatch] batch %r is done with failure" % section)
                if not status and _email_on_success:
                    LOGGER.debug("sending email for batch success")
                    LOGGER.send_email(file.read(), "[pybatch] batch %r is done with success" % section)
            return status
