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
				[nama, handphone, dokumen].forEach(el => {
					if(el.val() == '') {
						el.closest('.field').addClass('error');
						el.siblings('.ui.button').addClass('negative');
					}
				});
				if(nama.val() == '' || handphone.val() == '' || dokumen.val() == '') return false;
				$('form').submit();
			});
		}
	};

	this.admin = {};

	this.admin.common = {
		sidebar: () => {
			$('#sidebar-toggle').click(function () {
				$('.ui.sidebar').sidebar('toggle');
			});
		}
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
