const $ = CTFd.lib.$;

function deleteSelectedInvites(event) {
  let inviteIDs = $("input[data-invite-id]:checked").map(function() {
    return $(this).data("invite-id");
  });
  let target = inviteIDs.length === 1 ? "invite" : "invites";

  CTFd.ui.ezq.ezQuery({
    title: "Delete Invites",
    body: `Are you sure you want to delete ${inviteIDs.length} ${target}?`,
    success: function() {
      const reqs = [];
      for (var inviteID of inviteIDs) {
        reqs.push(
          CTFd.fetch(`/admin/bouncer/${inviteID}`, {
            method: "DELETE"
          })
        );
      }
      Promise.all(reqs).then(responses => {
        window.location.reload();
      });
    }
  });
}

$(() => {
  $("#invites-delete-button").click(deleteSelectedInvites);
});