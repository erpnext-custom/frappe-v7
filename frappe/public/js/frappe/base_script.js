window.frappe = {
    page_ready_events: {},
    ready: function(fn) {
        if (!frappe.page_ready_events[location.pathname]) {
            frappe.page_ready_events[location.pathname] = []
        }
        frappe.page_ready_events[location.pathname].push(fn);
    }
}
window.dev_server = {{ dev_server }};