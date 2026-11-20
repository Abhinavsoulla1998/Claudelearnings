#!/usr/bin/env bash
# bedrock-setup.sh
# Configures Claude Code to use AWS Bedrock instead of the direct Anthropic API.
# Run this script in your shell (or add the exports to ~/.bashrc / ~/.zshrc) before
# starting a Claude Code session.
#
# Prerequisites:
#   1. An AWS account with Amazon Bedrock enabled.
#   2. Bedrock model access approved for Claude models in your region.
#      (AWS Console > Amazon Bedrock > Model access > Request access)
#   3. IAM user or role with the following permissions:
#        - bedrock:InvokeModel
#        - bedrock:InvokeModelWithResponseStream
#      Scoped to the Claude model ARNs you intend to use:
#        arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-*
#
# Usage:
#   source bedrock-setup.sh          # apply exports to current shell
#   bash bedrock-setup.sh            # run in a subshell (exports won't persist)

set -euo pipefail

# ---------------------------------------------------------------------------
# AWS_ACCESS_KEY_ID
# The access key ID for the IAM user or role that has Bedrock permissions.
# For production use, prefer IAM roles with short-lived credentials via STS
# (e.g., aws sts assume-role) rather than long-lived access keys.
# ---------------------------------------------------------------------------
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-your-access-key-id-here}"

# ---------------------------------------------------------------------------
# AWS_SECRET_ACCESS_KEY
# The secret access key paired with AWS_ACCESS_KEY_ID.
# Never hard-code this value in a script committed to source control.
# Use a secrets manager (AWS Secrets Manager, HashiCorp Vault) or set it in
# your shell profile outside of version-controlled files.
# ---------------------------------------------------------------------------
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-your-secret-access-key-here}"

# ---------------------------------------------------------------------------
# AWS_SESSION_TOKEN (optional)
# Required when using temporary credentials from AWS STS (sts assume-role,
# sts get-session-token, or EC2/ECS instance profile). Leave unset if you are
# using long-lived IAM user credentials.
# ---------------------------------------------------------------------------
# export AWS_SESSION_TOKEN="your-session-token-here"

# ---------------------------------------------------------------------------
# AWS_REGION
# The AWS region where Amazon Bedrock is enabled and where Claude model access
# has been approved. Claude models are not available in all Bedrock regions.
# Supported regions (as of mid-2025): us-east-1, us-west-2, eu-west-1,
# ap-northeast-1. Check the Bedrock documentation for the current list.
# ---------------------------------------------------------------------------
export AWS_REGION="${AWS_REGION:-us-east-1}"

# ---------------------------------------------------------------------------
# CLAUDE_CODE_USE_BEDROCK
# When set to "true", Claude Code routes all API requests through AWS Bedrock
# instead of the direct Anthropic API. You do not need ANTHROPIC_API_KEY when
# using Bedrock — AWS credentials are used for authentication.
# ---------------------------------------------------------------------------
export CLAUDE_CODE_USE_BEDROCK=true

# ---------------------------------------------------------------------------
# Verify the configuration before starting Claude Code.
# ---------------------------------------------------------------------------
echo "Bedrock configuration:"
echo "  AWS_REGION:              $AWS_REGION"
echo "  CLAUDE_CODE_USE_BEDROCK: $CLAUDE_CODE_USE_BEDROCK"
echo "  AWS_ACCESS_KEY_ID:       ${AWS_ACCESS_KEY_ID:0:8}... (truncated)"

# Verify AWS CLI is available and credentials are valid.
if command -v aws &>/dev/null; then
    echo ""
    echo "Verifying AWS credentials..."
    if aws sts get-caller-identity --region "$AWS_REGION" --output table 2>&1; then
        echo "AWS credentials are valid."
    else
        echo "ERROR: AWS credentials are invalid or Bedrock is not accessible in $AWS_REGION." >&2
        echo "Check your IAM permissions and that Bedrock model access is approved." >&2
        exit 1
    fi
else
    echo "WARNING: AWS CLI not found. Skipping credential verification."
    echo "Install the AWS CLI to verify credentials: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
fi

echo ""
echo "Running a test query through Claude Code via Bedrock..."
echo "---"

# Run a simple non-interactive test query. The -p flag makes Claude Code exit
# after printing the response (non-interactive / headless mode).
claude -p "Say 'Bedrock connection successful' and nothing else." --output-format text

echo "---"
echo "Bedrock setup complete. You can now start Claude Code normally."
echo ""
echo "To make this permanent, add the export lines to ~/.bashrc or ~/.zshrc:"
echo "  export AWS_ACCESS_KEY_ID=..."
echo "  export AWS_SECRET_ACCESS_KEY=..."
echo "  export AWS_REGION=$AWS_REGION"
echo "  export CLAUDE_CODE_USE_BEDROCK=true"
