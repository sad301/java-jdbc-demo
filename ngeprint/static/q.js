function _() {

	this.index = {
		init: () => {
			$('input[type="text"]').focus(e => {
				$(e.target).closest('.field').removeClass('error');
				if(e.target.id == 'txt-dokumen') {
					$('#btn-select-file').removeClass('negative');
				}
			});
			$('input[name="dokumen"]').change(e => {
				$('#txt-dokumen').val(e.target.files[0].name);
			});
			$('#btn-select-file').click(e => {
				e.preventDefault();
				$('input[name="dokumen"]').trigger('click');
			});
			$('#btn-send').click(e => {
				e.preventDefault();
				let nama = $('input[name="nama"]');
				let handphone = $('input[name="handphone"]');
				let dokumen = $('input[name="dokumen"]');
				var formData = new FormData();
				[nama, handphone, dokumen].forEach(el => {
					if(el.val() == '') {
						el.closest('.field').addClass('error');
						el.siblings('.ui.button').addClass('negative');
					}
					if(el.attr('type') == 'text') formData.append(el.attr('name'), el.val());
					if(el.attr('type') == 'file') formData.append(el.attr('name'), el[0].files[0]);
				});
				if(nama.val() == '' || handphone.val() == '' || dokumen.val() == '') return false;
				let q = $.ajax({
					method: 'POST',
					url: '/api/jobs',
					data: formData,
					processData: false,
					contentType: false,
					beforeSend: () => $(e.target).addClass('loading')
				});
				q.done((data) => location.href = `/cost/${data.id}`);
				q.fail((xhr, status, err) => console.log(xhr.responseText));
			});
		}
	};

	/*
	 * -------------------------- *
	 * For use in url: /cost/<id> *
	 * -------------------------- *
	 */

	this.cost = {};
	this.cost.init = () => {
		let id = $('#params').data('id');
		let socket_io = io.connect('http://127.0.0.1:8000');
		socket_io.on('connect', (msg) => {
			socket_io.emit('client_connect', id);
		});
		socket_io.on('server_confirm', (msg) => {
			console.log(msg);
		});
		socket_io.on('process_done', (msg) => {
			console.log(msg);
		});
		$('#btn-agree').click(this.cost.agree);
		$('#btn-cancel').click(this.cost.cancel);
	};
	this.cost.agree = () => {
		console.log('agree');
	};
	this.cost.cancel = (e) => {
		let q = $.ajax({
			url: `/api/jobs/${$('#params').data('id')}`,
			method: 'DELETE',
			beforeSend: () => $(e.target).addClass('loading')
		});
		q.done(data => location.href = '/');
		q.fail((xhr, status, err) => console.log(xhr.responseText));
	};

	/*
	 * ------------------- *
	 * For use in : /admin *
	 * ------------------- *
	 */

	this.admin = {};
	this.admin.common = {};
	this.admin.common.sidebar = () => {
		$('#sidebar-toggle').click(function () {
			$('.ui.sidebar').sidebar('toggle');
		});
	};

	this.admin.home = {
		init: () => {
			this.admin.common.sidebar();
		}
	};

	this.admin.jobs = {
		init: () => {
			this.admin.common.sidebar();
		}
	};

}

_.q = function () {
	return new _();
};
