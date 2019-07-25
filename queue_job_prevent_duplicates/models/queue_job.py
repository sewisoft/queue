
from odoo import models, api
from odoo.addons.queue_job.fields import JobSerialized
from odoo.addons.queue_job.job import STARTED, DONE
import logging
_logger = logging.getLogger(__name__)


class QueueJob(models.Model):
    _inherit = 'queue.job'

    @api.model
    def domain_duplicate_jobs(self, vals):
        record_ids = vals['record_ids']
        model = repr(self.env[vals['model_name']].browse(record_ids))
        args = [repr(arg) for arg in vals['args']]
        kwargs = ['%s=%r' % (key, val) for key, val in list(vals['kwargs'].items())]
        all_args = ", ".join(args + kwargs)
        func_string = "%s.%s(%s)" % (model, vals['method_name'], all_args)

        return [
            ('state', 'not in', [STARTED, DONE]),
            ('func_string', 'like', func_string)
        ]

    @api.model
    def create(self, vals):

        # This lines are necessary, because the JobSerialized Field from the original Module does the same
        json_field = JobSerialized()
        vals['kwargs'] = json_field.convert_to_cache(json_field.convert_to_column(vals['kwargs'], self), self)
        vals['args'] = json_field.convert_to_cache(json_field.convert_to_column(vals['args'], self), self)

        dom = self.domain_duplicate_jobs(vals)

        if dom and self.env['queue.job'].search_count(dom):
            _logger.info("A job already exists for domain {}".format(dom))
            return

        return super(QueueJob, self).create(vals)