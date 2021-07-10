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
		socket_io.on('process_failed', (msg) => {
			alert(msg);
		});
		socket_io.on('process_done', (job) => {
			let idr = Intl.NumberFormat('id-ID', {style: 'currency', currency: 'IDR'});
			$('#client_file').val(job.client_file);
			['grayscale', 'color', 'blank'].forEach(p => {
				$('#'+p).empty().append([
					$('<td/>').text(p),
					$('<td/>',{'class':'right aligned'}).html(job['page_'+p]),
					$('<td/>',{'class':'right aligned'}).text(job['price_'+p] != 0 ? idr.format(job['price_'+p]) : job['price_'+p])
				]);
			});
			$('#total').empty().append([
				$('<th/>').html('&nbsp;'),
				$('<th/>',{'class':'right aligned'}).html(job['page_total']),
				$('<th/>',{'class':'right aligned'}).text(idr.format(job['price_total']))
			]);
			if(job.page_total > job.max_page) {
				$('table.ui.table').after($($('#warning-message-template').html()));
			}
			$('.ui.segment').removeClass('loading');
		});
		$('#btn-confirm').click(this.cost.confirm);
		$('#btn-cancel').click(this.cost.cancel);
	};
	this.cost.confirm = (e) => {
		$(e.target).addClass('loading');
		setTimeout(function () {
			location.href = `/confirm/${$('#params').data('id')}`;
		}, 1000);
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
	 * -----------------------------
	 * For use in url: /confirm/<id>
	 * -----------------------------
	 */

	this.confirm = {};
	this.confirm.init = () => {
		$('.twelve.digit').mask('AAAA-AAAA-AAAA').keyup((e) => {
			$(e.target).val($(e.target).val().toUpperCase());
			if($(e.target).val().length < 14) {
				$('button.ui.button').addClass('disabled');
			}
			else {
				$('button.ui.button').removeClass('disabled');
			}
		});
		$('button.ui.button').click((e) => {
			let jq = $.ajax({
				url: `/api/jobs/${$('#params').data('id')}/confirm`,
				method: 'PUT',
				data: {kode: $('input').val()},
				beforeSend: () => $(e.target).addClass('loading')
			});
			jq.done((data) => location.href = `/done/${$('#params').data('id')}`);
			jq.fail((xhr, status, err) => console.log(xhr.responseText));
		});
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

	this.admin.home = {};
	this.admin.home.init = () => {
		this.admin.common.sidebar();
	};

	this.admin.jobs = {};
	this.admin.jobs.ready = () => {
		let idr = Intl.NumberFormat('id-ID', {'style':'currency', 'currency':'IDR'});
		let jq = $.get('/api/jobs');
		jq.done(jobs => {
			let rows = [];
			let row_html = $('#row-template').html();
			jobs.forEach((job, i) => {
				let row = $(row_html);
				row.find('.ui.dropdown').dropdown();
				row.find('td:nth-child(1) a.ui.primary.button').attr('href', `/admin/jobs/${job.id}`);
				row.find('td:nth-child(2)').append(() => {
					let color = '';
					let status = job.status.toLowerCase();
					switch(status) {
						case 'confirmed': color = 'orange'; break;
						case 'printed': color = 'green'; break;
						case 'paid': color = 'blue'; break;
					}
					return $('<div/>',{'class':`ui ${color} label`}).text(status);
				});
				row.find('td:nth-child(3)').append(() => {
					let date = new Date(job.tanggal);
					return $('<div/>').append([
						$('<div/>',{'style':'font-weight: bold'}).text(date.toLocaleString('id', {day: '2-digit', month: 'long', year: 'numeric'})),
						$('<p/>').text(date.toLocaleString([], {hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false}))
					]);
				});
				row.find('td:nth-child(4)').append(() => {
					return $('<div/>').append([
						$('<div/>',{'style':'font-weight: bold'}).text(job.nama),
						$('<p/>').text(job.handphone)
					]);
				});
				row.find('td:nth-child(5)').append(() => {
					return $('<div/>',{'class':'ui transparent fluid left icon input'}).append([
						$('<i/>',{'class':'pdf file icon'}),
						$('<input/>',{'value':job.client_file})
					]);
				});
				row.find('td:nth-child(6)').append(() => {
					return $('<div/>').append([
						$('<div/>',{'style':'font-weight: bold'}).text(idr.format(job.price_total)),
						$('<p/>').text(`${job.page_total} lembar`)
					]);
				});
				rows.push(row);
			});
			$('table.ui.table tbody').empty().append(rows);
		});
	};
	this.admin.jobs.init = () => {
		this.admin.common.sidebar();
		$(document).ready(this.admin.jobs.ready);
	};

	this.admin.job = {};
	this.admin.job.ready = () => {
		let idr = Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR' });
		let id = $('#params').data('id');
		let jq = $.get(`/api/jobs/${id}`);
		jq.done((data) => {
			console.log(data);
			$('input[name="kode"]').val(data.kode);
			$('select[name="status"]').dropdown('set selected', data.status);
			$('input[name="tanggal"]').val(() => {
				let date = new Date(data.tanggal);
				let strDate = date.toLocaleString('id', {
					day: '2-digit',
					month: 'long',
					year: 'numeric'
				});
				let strTime = date.toLocaleString([], {
					hour: '2-digit',
					minute: '2-digit',
					hour12: false
				});
				return strDate + ', ' + strTime;
			});
			$('input[name="nama"]').val(data.nama);
			$('input[name="handphone"]').val(data.handphone);
			$('input[name="client_file"]').val(data.client_file);
			['grayscale', 'color', 'blank', 'total'].forEach((t) => {
				$(`td#page_${t}`).text(data[`page_${t}`]);
				$(`td#price_${t}`).text(data[`price_${t}`] > 0 ? idr.format(data[`price_${t}`]) : 0);
			});
		});
	};
	this.admin.job.init = () => {
		this.admin.common.sidebar();
		$('select.ui.dropdown').dropdown();
		$(document).ready(this.admin.job.ready);
	};

}

_.q = function () {
	return new _();
};
