# Cloud Cost Digest config
- `materiality_floor: 500`        # currency units of absolute change. Below this, ignore
- `comparison: previous calendar month`
- `ownership_dimension: tag:owner` # or account, subscription, resource group

## Owner mapping
Used when the ownership dimension is missing or unreadable.
- (tag value) -> (person)
