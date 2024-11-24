/**
 * SweetAlert2 adapter.
 * https://sweetalert2.github.io/
 */
ckan.module("snap-swal", function () {
  return {
    options: {},

    initialize() {
      // stop execution if dependency is missing.
      if (typeof Swal === "undefined") {
        // reporting the source of the problem is always a good idea.
        console.error(
          "[snap-swal] SweetAlert library is not loaded",
        );
        return;
      }

      const options = this.sandbox["snap"].nestedOptions(
        this.options,
      );
      this.el.on("click", () => Swal.fire(options));
    },
  };
});
