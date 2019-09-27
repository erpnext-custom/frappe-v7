from __future__ import unicode_literals
import frappe

##
# Cancelling draft documents
##
@frappe.whitelist()
def cancel_draft_doc(doctype, docname):
        # Updating Master table docstatus to 2
        doc = frappe.get_doc(doctype, docname)
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
	elif doctype == "Travel Claim":
		if doc.ta:
			ta = frappe.get_doc("Travel Authorization", doc.ta)
			ta.db_set("travel_claim", None)
	elif doctype == "Job Card":
		br = frappe.get_doc("Break Down Report", doc.break_down_report)
                br.db_set("job_card", None)
	elif doctype == "Asset":
		aid_name = frappe.db.get_value("Asset Issue Details", {"reference_code":doc.name , "docstatus":1}, "name")
                if aid_name:
                        frappe.db.sql("Update `tabAsset Issue Details` set reference_code = '', docstatus=2 where name = %s", aid_name)
                        frappe.msgprint("Asset No. {0} cancelled along with Asset Issue Details No {1} ".format(doc.name, aid_name))
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
