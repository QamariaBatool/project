# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class JobController(http.Controller):

    @http.route('/jobs/<int:job_id>', type='http', auth="public", website=True)
    def job_page(self, job_id, ref=None, **kwargs):
        job = request.env['hr.job'].sudo().browse(job_id)
        recruiter = request.env['res.users'].sudo().browse(int(ref)) if ref else None
        return request.render('hr_recruitment_extend.job_template', {
            'job': job,
            'recruiter': recruiter
        })

    @http.route('/jobs/apply/<int:job_id>', type='http', auth="public", website=True)
    def job_apply(self, job_id, ref=None, **kwargs):
        """Handles job application and stores recruiter reference"""
        job = request.env['hr.job'].sudo().browse(job_id)
        recruiter_id = int(ref) if ref else None

        applicant_vals = {
            'job_id': job.id,
            'name': job.name,
            'partner_id': request.env.user.partner_id.id,  # Applicant
            'recruiter_id': recruiter_id,  # Store recruiter reference
        }

        request.env['hr.applicant'].sudo().create(applicant_vals)
        return request.render('hr_recruitment_extend.job_thank_you_template')

