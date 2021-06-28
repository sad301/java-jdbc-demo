function _() {
	this.index = function () {
		$('input[type=file]').change(e => {
			let f = e.target.files[0];
			$('#txt-dokumen').val(f.name);
		});
		$('#btn-select-file').click(e => {
			$('input[type="file"]').trigger('click');
		});
	}
}

_.q = function () {
	return new _();
};
