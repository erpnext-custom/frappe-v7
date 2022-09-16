frappe.ui.form.on("Version", "refresh", function(frm) {
	$(frappe.render_template('version_view', {doc:frm.doc, data:JSON.parse(frm.doc.data)}))
		.appendTo(frm.fields_dict.table_html.$wrapper.empty());

	frm.add_custom_button(__('Show all Versions'), function() {
		frappe.set_route('List', 'Version',
			{ref_doctype: frm.doc.ref_doctype, docname: frm.doc.docname});
	});
});

/*frappe.ui.form.on("Version", "refresh", function(frm) {
	frm.add_custom_button("Restore", function() {
		frappe.call({
			method:"frappe.core.doctype.version.version.restore",
			args: {
				version: frm.doc.name
			},
			callback: function(r) {
				if(!r.exc) {
					msgprint(__("Version restored"));
				}
			}
		})
	});
})*/
