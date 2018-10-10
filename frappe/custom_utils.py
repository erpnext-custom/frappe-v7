from __future__ import unicode_literals
import frappe

##
# Cancelling draft documents
##
@frappe.whitelist()
def cancel_draft_doc(doctype, docname):
        doc = frappe.get_doc(doctype, docname)
        doc.db_set("docstatus", 2)
	if doctype == "Material Request":
		doc.db_set("status", "Cancelled")
		doc.db_set("workflow_state", "Cancelled")
	elif doctype == "Travel Claim":
		if doc.ta:
			ta = frappe.get_doc("Travel Authorization", doc.ta)
			ta.db_set("travel_claim", "")
	elif doctype == "Imprest Recoup":
                doc.db_set("workflow_state", "Cancelled")
        elif doctype == "Imprest Receipt":
                doc.db_set("workflow_state", "Cancelled")
        elif doctype == "Job Card":
		br = frappe.get_doc("Break Down Report", doc.break_down_report)
                br.db_set("job_card", "")
        elif doctype == "Overtime Application":
                doc.db_set("workflow_state", "Cancelled")
        else:
                pass
                
