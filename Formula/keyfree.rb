class Keyfree < Formula
  desc "Find free macOS keyboard shortcuts and check whether one is taken"
  homepage "https://github.com/samliebl/keyfree"
  url "https://github.com/samliebl/keyfree/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "REPLACE_WITH_SHA256_AFTER_TAGGING"
  license "MIT"
  head "https://github.com/samliebl/keyfree.git", branch: "main"

  depends_on :macos
  depends_on "bash"

  def install
    inreplace "bin/keyfree", "#!/usr/bin/env bash", "#!#{Formula["bash"].opt_bin}/bash"
    bin.install "bin/keyfree"
  end

  test do
    assert_match "keyfree #{version}", shell_output("#{bin}/keyfree --version")
    assert_match "taken", shell_output("#{bin}/keyfree check cmd+q --plain", 1)
  end
end
