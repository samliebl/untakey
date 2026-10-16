class Untakey < Formula
  desc "Find free macOS keyboard shortcuts and check whether one is taken"
  homepage "https://github.com/samliebl/untakey"
  url "https://github.com/samliebl/untakey/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "REPLACE_WITH_SHA256_AFTER_TAGGING"
  license "MIT"
  head "https://github.com/samliebl/untakey.git", branch: "main"

  depends_on :macos
  depends_on "bash"

  def install
    inreplace "bin/untakey", "#!/usr/bin/env bash", "#!#{Formula["bash"].opt_bin}/bash"
    bin.install "bin/untakey"
  end

  test do
    assert_match "untakey #{version}", shell_output("#{bin}/untakey --version")
    assert_match "taken", shell_output("#{bin}/untakey check cmd+q --plain", 1)
  end
end
