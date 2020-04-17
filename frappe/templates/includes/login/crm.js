// login.js
// don't remove this line (used in test)

window.disable_signup = {{ disable_signup and "true" or "false" }};

window.login = {};

login.bind_events = function() {
	$(window).on("hashchange", function() {
		login.route();
	});

	$(".form-login").on("submit", function(event) {
		event.preventDefault();
		var args = {};
		args.cmd = "login";
		args.usr = ($("#login_email").val() || "").trim();
		args.pwd = $("#login_password").val();
		args.device = "desktop";
		if(!args.usr || !args.pwd) {
			frappe.msgprint(__("Both login and password required"));
			return false;
		}
		login.call(args);
		return false;
	});

	$(".form-signup").on("submit", function(event) {
		event.preventDefault();
		var args = {};
		args.cmd = "frappe.core.doctype.user.user.crm_sign_up";
		args.full_name = ($("#signup_fullname").val() || "").trim();
		args.login_id = ($("#signup_login_id").val() || "").trim();
		args.mobile_no = ($("#signup_mobile_no").val() || "").trim();
		args.alternate_mobile_no = ($("#signup_alternate_mobile_no").val() || "").trim();
		args.email = ($("#signup_email").val() || "").trim();
		args.pin = ($("#signup_pin").val() || "").trim();
		if(!args.full_name) {
			frappe.msgprint(__("Valid name required"));
			return false;
		} else if(!args.login_id) {
			frappe.msgprint(__("Valid CID/LicenseNo name required"));
			return false;
		} else if(!args.mobile_no) {
			frappe.msgprint(__("Valid mobile number required"));
			return false;
		} else if(args.email && !valid_email(args.email)) {
			frappe.msgprint(__("Valid email required"));
			return false;
		} else if(!args.pin) {
			frappe.msgprint(__("Valid PIN required. If you do not have one, please click on <b>Get your PIN</b> below."));
			return false;
		}
		login.call(args);
		return false;
	});

	$(".btn-pin").click(function(){
		event.preventDefault();
		var args = {};
		args.cmd = "frappe.core.doctype.user.user.send_pin";
		args.full_name  = ($("#signup_fullname").val() || "").trim();
		args.login_id  = ($("#signup_login_id").val() || "").trim();
		args.mobile_no = ($("#signup_mobile_no").val() || "").trim();
		if(!args.full_name || !args.login_id || !args.mobile_no) {
			frappe.msgprint(__("Valid Full Name,CID/LicenseNo and Mobile Number required"));
			return false;
		}
		login.call(args);
		return false;
	});

	$(".form-forgot").on("submit", function(event) {
		event.preventDefault();
		var args = {};
		args.cmd = "frappe.core.doctype.user.user.crm_reset_password";
		args.login_id = ($("#forgot_login_id").val() || "").trim();
		args.mobile_no = ($("#forgot_mobile_no").val() || "").trim();
		if(!args.login_id || !args.mobile_no) {
			frappe.msgprint(__("Valid CID/LincenseNo and Mobile Number required."));
			return false;
		}
		login.call(args);
		return false;
	});
}


login.route = function() {
	var route = window.location.hash.slice(1);
	if(!route) route = "login";
	login[route]();
}

login.login = function() {
	$("form").toggle(false);
	$(".form-login").toggle(true);
}

login.forgot = function() {
	$("form").toggle(false);
	$(".form-forgot").toggle(true);
}

login.signup = function() {
	$("form").toggle(false);
	$(".form-signup").toggle(true);
}


// Login
login.call = function(args) {
	return frappe.call({
		type: "POST",
		args: args,
		freeze: true,
		statusCode: login.login_handlers
	});
}

login.login_handlers = (function() {
	var get_error_handler = function(default_message) {
		return function(xhr, data) {
			if(xhr.responseJSON) {
				data = xhr.responseJSON;
			}

			var message = default_message;
			if (data._server_messages) {
				message = ($.map(JSON.parse(data._server_messages || '[]'), function() {
					// temp fix for messages sent as dict
					try {
						return JSON.parse(v).message;
					} catch (e) {
						return v;
					}
				}) || []).join('<br>') || default_message;
			}

			frappe.msgprint(message);
		};
	}

	var login_handlers = {
		200: function(data) {
			if(data.message=="Logged In") {
				window.location.href = get_url_arg("redirect-to") || data.home_page;
			} else if(data.message=="No App") {
				if(localStorage) {
					var last_visited =
						localStorage.getItem("last_visited")
						|| get_url_arg("redirect-to");
					localStorage.removeItem("last_visited");
				}

				if(last_visited && last_visited != "/login") {
					window.location.href = last_visited;
				} else {
					window.location.href = data.home_page;
				}
			} else if(["#signup", "#forgot"].indexOf(window.location.hash)!==-1) {
				frappe.msgprint(data.message);
			}
		},
		401: get_error_handler(__("Invalid Login")),
		417: get_error_handler(__("Oops! Something went wrong"))
	};

	return login_handlers;
})();

frappe.ready(function() {
	login.bind_events();

	if (!window.location.hash) {
		window.location.hash = "#login";
	} else {
		$(window).trigger("hashchange");
	}

	$(".form-signup, .form-forgot").removeClass("hide");
	$(document).trigger('login_rendered');
});
