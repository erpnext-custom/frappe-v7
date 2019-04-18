'''
--------------------------------------------------------------------------------------------------------------------------
Version          Author          CreatedOn          ModifiedOn          Remarks
------------ --------------- ------------------ -------------------  -----------------------------------------------------
2.0.190225        SHIV                             25/02/2018         * cancel_draft_doc()
                                                                        * code of `Leave Application` added
--------------------------------------------------------------------------------------------------------------------------                                                                          
'''
from __future__ import unicode_literals
import frappe
from frappe import _

##
# Cancelling draft documents
##
@frappe.whitelist()
def cancel_draft_doc(doctype, docname):
        # Updating Master table docstatus to 2
        doc = frappe.get_doc(doctype, docname)
        if doctype == "Leave Application":    ##### Ver 2.0.190225 added by SHIV
                if doc.get("workflow_state") not in ("Draft","Rejected") and frappe.session.user not in (doc.get("leave_approver"),"Administrator"):
                        frappe.throw(_("Only leave approver <b>{0}</b> ( {1} ) can cancel this document.").format(doc.leave_approver_name, doc.leave_approver), title="Operation not permitted")
        doc.db_set("docstatus", 2)

        # Updating Child tables docstatus to 2
        meta = frappe.get_meta(doctype)
        if not meta.issingle:
                if not meta.istable:
                        for df in meta.get_table_fields():
                                frappe.db.sql("""update `tab{0}` set docstatus=2 where parent='{1}'""".format(df.options,docname))

        if frappe.db.exists("Workflow", doctype):
                wfs = frappe.db.get_values("Workflow Document State", {"parent":doctype, "doc_status": 2}, "state", as_dict=True)
                doc.db_set("workflow_state", wfs[0].state if len(wfs) == 1 else "Cancelled")


        if doctype == "Material Request":
		doc.db_set("status", "Cancelled")
	elif doctype == "Leave Application":    ##### Ver 2.0.190225 added by SHIV
		doc.db_set("status", "Cancelled")
	elif doctype == "Travel Claim":
		if doc.ta:
			ta = frappe.get_doc("Travel Authorization", doc.ta)
			ta.db_set("travel_claim", None)
	elif doctype == "Job Card":
		br = frappe.get_doc("Break Down Report", doc.break_down_report)
                br.db_set("job_card", None)
        else:
                pass

        '''
	if doctype == "Material Request":
		doc.db_set("status", "Cancelled")
		doc.db_set("workflow_state", "Cancelled")
	elif doctype == "Travel Claim":
		if doc.ta:
			ta = frappe.get_doc("Travel Authorization", doc.ta)
			ta.db_set("travel_claim", None)
	elif doctype == "Imprest Recoup":
                doc.db_set("workflow_state", "Cancelled")
        elif doctype == "Imprest Receipt":
                doc.db_set("workflow_state", "Cancelled")
        elif doctype == "Job Card":
		br = frappe.get_doc("Break Down Report", doc.break_down_report)
                br.db_set("job_card", None)
        elif doctype == "Overtime Application":
                doc.db_set("workflow_state", "Cancelled")
	elif doctype == "Fund Requisition":
		doc.db_set("workflow_state", "Cancelled")
        else:
                pass     
        '''
