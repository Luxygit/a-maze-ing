
# Variables
NAME        = a_maze_ing.py
VENV        = .venv
PYTHON      = $(VENV)/bin/python3
PIP         = $(VENV)/bin/pip3

# Default testing arguments (Width Height Seed Perfect)
DEFAULT_ARGS = config.txt

# Colors for clean terminal feedback
GREEN       = \033[0;32m
RED         = \033[0;31m
RESET       = \033[0m

all: $(VENV)
	@echo "$(GREEN)Entering runtime environment...$(RESET)"
	@echo "To run with your own arguments, use: make run ARGS=\"w h seed perfect\""
	$(PYTHON) $(NAME) $(DEFAULT_ARGS)

# 1. Automatically create virtual environment and compile/install local mlx
$(VENV):
	@echo "$(GREEN)Initializing local Python Virtual Environment...$(RESET)"
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	@if [ -f *.whl ]; then \
		echo "$(GREEN)Found MiniLibX Wheel asset. Installing to venv...$(RESET)"; \
		$(PIP) install *.whl; \
	elif [ -f Makefile ]; then \
		echo "$(GREEN)No Wheel found. Checking local library directory...$(RESET)"; \
	fi

# 2. Flexible running command rule supporting customized variables override
run: $(VENV)
	$(PYTHON) $(NAME) $(ARGS)

# 3. Clean up temporary zombie background process locks
clean:
	@echo "$(RED)Clearing hanging Python window threads...$(RESET)"
	@pkill -9 -f $(NAME) > /dev/null 2>&1 || true

# 4. Deep cleanup removing the entire virtual environment setup
fclean: clean
	@echo "$(RED)Removing Virtual Environment directory...$(RESET)"
	@rm -rf $(VENV)
	@rm -rf __pycache__ */__pycache__

# 5. Full re-initialization pipeline rule tracking configuration updates
re: fclean all

.PHONY: all run clean fclean re
